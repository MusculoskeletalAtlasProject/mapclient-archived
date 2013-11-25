'''
Created on Jun 20, 2013

@author: hsorby
'''

from requests_oauthlib import OAuth1Session

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

def make_form_request(action=None, **kw):
    return {
        'fields': kw,
        'actions': {action: True},
    }


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

    def make_session(self, pmr_info):
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
    # redirects while using allow_redirect=False when making all requests

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

    def addWorkspace(self, title, description):
        session = self.make_session()

    def cloneWorkspace(self, source_url, target_dir):
        pass

    def linkWorkspaceDirToUrl(self, local_workspace_dir, remote_workspace_url):
        # links a non-pmr workspace dir to a remote workspace url.
        # prereq is that the remote must be new.
        pass
