'''
Created on Jun 20, 2013

@author: hsorby
'''

import json
import logging

from requests import HTTPError
from requests import Session
from requests_oauthlib import OAuth1Session
from simplejson import JSONDecodeError

from pmr.wfctrl.core import get_cmd_by_name
from pmr.wfctrl.core import CmdWorkspace

# This ensures the get_cmd_by_name will work, as any classes that needs
# to be registered has to be imported first, usually at the module level.
import pmr.wfctrl.cmd

from mapclient.exceptions import ClientRuntimeError
from mapclient.settings import info
from mapclient.tools.pmr.authoriseapplicationdialog import AuthoriseApplicationDialog

logger = logging.getLogger(__name__)

endpoints = {
    '': {
        'dashboard': 'pmr2-dashboard',
        'search': 'search',
    },

    'WorkspaceContainer': {
        'add-workspace': '+/addWorkspace',
    },

    'Workspace': {
        'temppass': 'request_temporary_password',
    },

}

def make_form_request(action_=None, **kw):
    return json.dumps({
        'fields': kw,
        'actions': {action_: 1},
    })



class PMRToolError(ClientRuntimeError):
    pass


class PMRTool(object):
    '''
    classdocs
    '''

    PROTOCOL = 'application/vnd.physiome.pmr2.json.0'
    UA = 'pmr.jsonclient.Client/0.2'

    def __init__(self):
        '''
        Constructor
        '''

    def make_session(self, pmr_info=None):
        if pmr_info is None:
            pmr_info = info.PMRInfo()

        if self.hasAccess():
            kwargs = pmr_info.get_session_kwargs()
            session = OAuth1Session(**kwargs)
        else:
            # normal session without OAuth requirements.
            session = Session()

        session.headers.update({
            'Accept': self.PROTOCOL,
            'Content-Type': self.PROTOCOL,
            'User-Agent': self.UA,
        })
        return session

    def hasAccess(self):
        pmr_info = info.PMRInfo()
        return pmr_info.has_access()

    # also workaround the resigning redirections by manually resolving
    # redirects while using allow_redirects=False when making all requests

    def _search(self, text):
        pmr_info = info.PMRInfo()
        session = self.make_session()
        data = json.dumps({'SearchableText': text, 'portal_type': 'Workspace'})
        r = session.post(
            '/'.join((pmr_info.host, endpoints['']['search'])),
            data=data,
        )
        r.raise_for_status()
        return r.json()

    def search(self, text):
        try:
            return self._search(text)
        except HTTPError as e:
            msg_403 = 'The configured PMR server may have disallowed searching.'
            if self.hasAccess():
                msg_403 = (
                    'Access credentials have become longer valid.  Please '
                    'deregister and register the application to renew access '
                    'and try again.'
                )
            if e.response.status_code == 403:
                raise PMRToolError('Permission Error', msg_403)
            else:
                raise PMRToolError('Web Service Error',
                    'The PMR search service may be misconfigured and/or '
                    'is unavailable at this moment.  Please check '
                    'configuration settings and try again.'
                )
        except JSONDecodeError:
            raise PMRToolError('Unexpected Server Response',
                'The server returned an unexpected response and MAP Client is '
                'unable to proceed.'
            )
        except Exception as e:
            raise PMRToolError('Unexpected exception', str(e))

    def _getObjectInfo(self, target_url):
        session = self.make_session()
        r = session.get(target_url)
        r.raise_for_status()
        return r.json()

    def getObjectInfo(self, target_url):
        try:
            return self._getObjectInfo(target_url)
        except HTTPError as e:
            raise PMRToolError('Remote server error',
                'Server responded with an error message and MAP Client is '
                'unable to continue the action.')
        except JSONDecodeError:
            raise PMRToolError('Unexpected Server Response',
                'The server returned an unexpected response that MAP Client '
                'cannot process.')
        except Exception as e:
            raise PMRToolError('Unexpected exception', str(e))

    def requestTemporaryPassword(self, workspace_url):
        if not self.hasAccess():
            return None

        session = self.make_session()
        r = session.post(
            '/'.join((workspace_url, endpoints['Workspace']['temppass'])),
            data='{}',
        )
        r.raise_for_status()
        return r.json()

    def authorizationUrl(self, key):
        return self._client.authorizationUrl(key)

    def getDashboard(self):
        pmr_info = info.PMRInfo()
        session = self.make_session(pmr_info)
        target = '/'.join([pmr_info.host, endpoints['']['dashboard']])
        r = session.get(target)
        r.raise_for_status()
        return r.json()

    def addWorkspace(self, title, description, storage='mercurial'):
        session = self.make_session()

        dashboard = self.getDashboard()
        option = dashboard.get('workspace-add', {})
        target = option.get('target')

        if target is None:
            # XXX exception?
            return

        # XXX until requests and requests_oauthlib work together to
        # provide a fix for the redirection and OAuth signature
        # regeneration, we have to handle all redirects manually.
        r = session.get(target, allow_redirects=False)
        target = r.headers.get('Location')

        # the real form get
        # XXX I need to get PMR to generate IDs if the autoinc isn't
        # enabled.
        # XXX should verify the contents of the fields.
        # r = session.get(target, allow_redirects=False)

        # For now, just post
        r = session.post(target,
            data=make_form_request('add',
                title=title,
                description=description,
                storage=storage,
            ),
            allow_redirects=False)

        workspace_target = r.headers.get('Location')
        # verify that this is an actual workspace by getting it.
        r = session.get(workspace_target)
        return r.json().get('url')

    def cloneWorkspace(self, remote_workspace_url, local_workspace_dir):
        # XXX target_dir is assumed to exist, so we can't just clone
        # but we have to instantiate that as a new repo, define the
        # remote and pull.

        # link
        self.linkWorkspaceDirToUrl(
            local_workspace_dir=local_workspace_dir,
            remote_workspace_url=remote_workspace_url,
        )

        workspace = CmdWorkspace(local_workspace_dir, auto=True)

        # Another caveat: that workspace is possibly private.  Acquire
        # temporary password.
        creds = self.requestTemporaryPassword(remote_workspace_url)
        if creds:
            result = workspace.cmd.pull(workspace,
                username=creds['user'], password=creds['key'])
        else:
            # no credentials
            logger.info('not using credentials as none are detected')
            result = workspace.cmd.pull(workspace)

        # TODO trap this result too?
        workspace.cmd.reset_to_remote(workspace)
        return result

    def linkWorkspaceDirToUrl(self, local_workspace_dir, remote_workspace_url):
        # links a non-pmr workspace dir to a remote workspace url.
        # prereq is that the remote must be new.

        # XXX should assert availability of storage
        # XXX figure out if/when/how to offer Git.

        workspace_obj = self.getObjectInfo(remote_workspace_url)
        # XXX only supporting mercurial now even though we can clone both
        cmd_cls = get_cmd_by_name(workspace_obj.get('storage'))
        if cmd_cls is None:
            raise PMRToolError('Remote storage format unsupported',
                'The remote storage `%(storage)s` is not one of the ones that '
                'the MAP Client currently supports.' % workspace_obj)

        # brand new command module for init.
        new_cmd = cmd_cls()
        workspace = CmdWorkspace(local_workspace_dir, new_cmd)

        # Add the remote using a new command
        cmd = cmd_cls(remote=remote_workspace_url)

        # Do the writing.
        cmd.write_remote(workspace)

    def hasDVCS(self, local_workspace_dir):
        workspace = CmdWorkspace(local_workspace_dir, auto=True)
        return workspace.cmd is not None

    def commitFiles(self, local_workspace_dir, message, files):
        workspace = CmdWorkspace(local_workspace_dir, auto=True)
        cmd = workspace.cmd
        if cmd is None:
            logger.info('skipping commit, no underlying repo detected')
            return

        logger.info('Using `%s` for committing files.', cmd.__class__.__name__)

        for fn in files:
            sout, serr = cmd.add(workspace, fn)
            # if serr has something we need to handle?
        
        # XXX committer will be a problem if unset in git.
        return cmd.commit(workspace, message)

    def pushToRemote(self, local_workspace_dir, remote_workspace_url=None):
        workspace = CmdWorkspace(local_workspace_dir, auto=True)

        if remote_workspace_url is None:
            remote_workspace_url = cmd.read_remote(workspace)
        # acquire temporary creds
        creds = self.requestTemporaryPassword(remote_workspace_url)

        stdout, stderr = cmd.push(workspace,
            username=creds['user'], password=creds['key'])

        if stderr:
            raise PMRToolError('Error pushing changes to PMR',
                'The command line tool gave us this error message:\n\n' +
                    stderr)

        return result
