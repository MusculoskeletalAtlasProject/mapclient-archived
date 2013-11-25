'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland

This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
import webbrowser
import logging
from PySide import QtGui

from mapclient.settings import info
from mapclient.tools.pmr.core import TokenHelper
from mapclient.tools.pmr.authoriseapplicationdialog import AuthoriseApplicationDialog
from mapclient.tools.pmr.ui_oauthcheckdialog import Ui_OAuthCheckDialog

logger = logging.getLogger(__name__)


class OAuthCheckDialog(QtGui.QDialog):
    """
    Dialog that other UI elements can spawn to check for existence of
    token credentials and acquire one from user if it is unavailable.
    """

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self._ui = Ui_OAuthCheckDialog()
        self._ui.setupUi(self)
        self._makeConnections()

    def _makeConnections(self):
        self._ui.continueButton.clicked.connect(self.event_register)

    def token(self):
        return self._ui.tokenLineEdit.text()

    def event_register(self, **kw):
        pmr_info = info.PMRInfo()

        helper = kw.pop('helper', None)
        browser = kw.pop('browser', webbrowser)

        if helper is None:
            helper = TokenHelper(
                client_key=pmr_info.consumer_public_token,
                client_secret=pmr_info.consumer_secret_token,
                site_url=pmr_info.host,
            )

        try:
            helper.get_temporary_credentials()
        except ValueError:
            QtGui.QMessageBox.information(self, 'Invalid Client Credentials',
                'Failed to retrieve temporary credentials.')
            return False

        url = helper.get_authorize_url()
        browser.open(url)
        # this should be the correct name for this dialog
        # dlg = OAuthVerifierDialog(self)
        dlg = AuthoriseApplicationDialog(self)
        dlg.setModal(True)
        if not dlg.exec_():
            return False

        verifier = dlg.token()
        helper.set_verifier(verifier)

        try:
            token_credentials = helper.get_token_credentials()
        except ValueError:
            QtGui.QMessageBox.information(self, 'Invalid Verifier',
                'Failed to retrieve token access with verification code.')
            return False

        logger.debug('token: %r', token_credentials)

        pmr_info.update_token(**token_credentials)

        return True
