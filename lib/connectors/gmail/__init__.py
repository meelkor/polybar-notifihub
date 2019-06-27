import os.path
import json
from apiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from lib.connectors.connection import BaseConnection
from lib.notification import NotificationSnapshot


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify']


class GmailConnection(BaseConnection):
    name = 'gmail'
    icon = '\uf0e0'

    _known_messages = {}
    _client = None


    def __init__(self, label, authConf):
        BaseConnection.__init__(self, label)

        credentials = Credentials(authConf['token'], authConf['refresh_token'],
                authConf['id_token'], authConf['token_uri'],
                authConf['client_id'], authConf['client_secret'],
                authConf['scopes'])
        self._client = discovery.build('gmail', 'v1', credentials=credentials)


    def update(self) -> list:
        messagesQuery = self._client.users().messages().list(
                userId='me', q='is:unread').execute()

        count = messagesQuery['resultSizeEstimate']

        if (count == 0):
            return NotificationSnapshot([])

        msg_ids = [msg['id'] for msg in messagesQuery['messages'][:5]]

        notifications = [self._get_or_load_message(id) for id in msg_ids]

        self._known_messages = dict((n.id, n) for n in notifications)

        return NotificationSnapshot(notifications, count)


    def dismiss(self, id: str):
        self._client.users().messages().modify(userId='me', id=id,
                body={'removeLabelIds': ['UNREAD']}).execute()


    def _get_or_load_message(self, msg_id):
        if (msg_id in self._known_messages):
            return self._known_messages[msg_id]

        email_detail = self._client.users().messages().get(
                userId='me', id=msg_id, format='metadata',
                metadataHeaders=['Subject']).execute()

        return self._make_notification(id=msg_id,
                title=self._get_subject(email_detail),
                detail=email_detail['snippet'])


    def _get_subject(self, email_detail):
        headers = email_detail['payload']['headers']
        return next(h for h in headers if h['name'] == 'Subject')['value']


    @staticmethod
    def authenticate():
        creds_path = os.path.join(os.path.dirname(__file__), './credentials.json')

        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server()

        creds_dict = { 'token': creds.token,
                'refresh_token': creds.refresh_token,
                'id_token': creds.id_token,
                'scopes': creds.scopes,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret }

        return creds_dict
