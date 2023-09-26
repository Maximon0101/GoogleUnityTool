import os.path

from google.auth.transport import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDriveAdapter:
    SCOPES = ['https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file']

    def __init__(self, name):
        self.name = name
        self.credentials = None
        secret_path = f"secrets/{name}.secret.json"
        token_path = f"secrets/{name}.token.json"

        # Initialisation
        print(f"Initialising GoogleDriveAdapter <{name}>")
        # Is file with token in folder
        if not os.path.exists(secret_path):
            raise RuntimeError(f"secret fo {name} didn't found")

        # Refreshing token if need it
        if os.path.exists(token_path):
            print("Loading credentials from token")
            self.credentials = Credentials.from_authorized_user_file(token_path, GoogleDriveAdapter.SCOPES)

        # Create token
        if not self.credentials or not self.credentials.valid:
            # If have no it
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print(f"refresh token <{name}>")
                self.credentials.refresh(Request())
            # If it invalid
            else:
                print(f"asking for token <{name}>")
                flow = InstalledAppFlow.from_client_secrets_file(
                    secret_path, GoogleDriveAdapter.SCOPES)
                self.credentials = flow.run_local_server(port=0)
            # Create new
            print(f"writing token file <{token_path}>")
            with open(token_path, 'w') as token_file:
                token_file.write(self.credentials.to_json())

        try:
            print("building google services")
            self.service = build('drive', 'v3', credentials=self.credentials)
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            raise RuntimeError
        print(f"GoogleDriveAdapter <{name}> initialised")
