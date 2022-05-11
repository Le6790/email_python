from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.compose']

class GmailEmail:
    def __init__(self):
        
        self.creds = self._get_creds()
        self.service = build('gmail', 'v1', credentials=self.creds)
    
    def _get_creds(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If there is no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials.json, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the redentials for the next run
            with open('token.json','w') as token:
                token.write(creds.to_json())
        
        return creds

    def get_labels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels',[])

        if not labels:
            return("No labels found")
        
        print('labels: ')
        for label in labels:
            print(label['name'])

        return labels
    
    def send_text_email(self, to_email, from_email, subject, message):
        msg = MIMEText(message)

        msg["subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        
        raw = base64.urlsafe_b64encode(msg.as_bytes())
        raw= raw.decode()
        body = {'raw':raw}

        msg = (self.service.users().messages().send(userId='me', body=body).execute())
        print(msg)

