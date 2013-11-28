'''
Created on Jun 20, 2013

@author: hsorby
'''

import json

from requests_oauthlib import OAuth1Session

from pmr.wfctrl.cmd import MercurialDvcsCmd
from pmr.wfctrl.core import CmdWorkspace

from mapclient.settings import info
from mapclient.tools.pmr.jsonclient.client import Client
from mapclient.tools.pmr.authoriseapplicationdialog import AuthoriseApplicationDialog

endpoints = {
    '': {
        'dashboard': 'pmr2-dashboard',
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
        kwargs = pmr_info.get_session_kwargs()
        session = OAuth1Session(**kwargs)
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

    def search(self, text):
        return self._client.search(text)

    def requestTemporaryPassword(self, workspace_url):
        return self._client.requestTemporaryPassword(workspace_url)

    def authorizationUrl(self, key):
        return self._client.authorizationUrl(key)

    def getDashboard(self):
        pmr_info = info.PMRInfo()
        session = self.make_session(pmr_info)
        target = '/'.join([pmr_info.host, endpoints['']['dashboard']])
        return session.get(target).json()

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

    def cloneWorkspace(self, source_url, target_dir):
        pass

    def linkWorkspaceDirToUrl(self, local_workspace_dir, remote_workspace_url):
        # links a non-pmr workspace dir to a remote workspace url.
        # prereq is that the remote must be new.

        # XXX should assert availability of Mercurial

        # brand new command module for init.
        new_cmd = MercurialDvcsCmd()
        workspace = CmdWorkspace(local_workspace_dir, new_cmd)

        # Add the remote using a new command
        cmd = MercurialDvcsCmd(remote=remote_workspace_url)

        # Do the writing.
        cmd.write_remote(workspace)
