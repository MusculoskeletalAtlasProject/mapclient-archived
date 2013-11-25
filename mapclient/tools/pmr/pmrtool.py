'''
Created on Jun 20, 2013

@author: hsorby
'''

from mapclient.settings import info
from mapclient.tools.pmr.jsonclient.client import Client
from mapclient.tools.pmr.authoriseapplicationdialog import AuthoriseApplicationDialog


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

        self._client_credentials = {
            'client_key': info.DEFAULT_CONSUMER_PUBLIC_TOKEN,
            'client_secret': info.DEFAULT_CONSUMER_SECRET_TOKEN,
        }

        self._token_credentials = {}

    def make_session(self):
        kwargs = {}
        kwargs.update(self._client_credentials)
        kwargs.update(self._token_credentials)

        session = OAuth1Session(**kwargs)
        session.headers.update({
            'Accept': self.PROTOCOL,
            'Content-Type': self.PROTOCOL,
            'User-Agent': self.UA,
        })
        return session

    def update_session(self):
        self.session = self.make_session()
        return self.session

    def hasAccess(self):
        pmr_info = info.PMRInfo()
        return pmr_info.has_access()

    # XXX clean up read/writing of tokens somewhere else.
    # consolidate the requests to use OAuth1Session
    # also workaround the resigning redirections by manually resolving
    # redirects while using allow_redirect=False when making all requests

    def search(self, text):
        return self._client.search(text)

    def requestTemporaryPassword(self, workspace_url):
        return self._client.requestTemporaryPassword(workspace_url)

    def requestTemporaryCredential(self):
        return self._client.requestTemporaryCredential()

    def authorizationUrl(self, key):
        return self._client.authorizationUrl(key)

    def getDashboard(self):
        raise NotImplementedError

    def addWorkspace(self, title, description):
        return self._client.addWorkspace(title, description)
