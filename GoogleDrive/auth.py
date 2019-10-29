from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class auth:
    """
    Class for loggin into Google drive
    """
    def __init__(self, SCOPES, SECRET_FILE, APPLICATION_NAME):
        self.__SCOPES = SCOPES
        self.__SECRET_FILE = SECRET_FILE
        self.__APPLICATION_NAME = APPLICATION_NAME
        
    def getCredentials(self):
        """
        Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the 0Auth2 flow is completed to obtain the new credentials.
        
        Returns:
            credentials, the obtained credential
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__SECRET_FILE, self.__SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                
        return creds

        # service = build('drive', 'v3', credentials=creds)
        
