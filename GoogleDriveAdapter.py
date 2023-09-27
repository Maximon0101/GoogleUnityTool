import hashlib
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class GoogleDriveAdapter:
    SCOPES = ['https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file']

    # Size of buffer for checksum
    BUF_SIZE = 65536  # this is bytes

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

        # Errors
        try:
            print("building google services")
            self.service = build('drive', 'v3', credentials=self.credentials)
        except HttpError:
            # TODO(developer) - Handle errors from drive API.
            raise RuntimeError
        print(f"GoogleDriveAdapter <{name}> initialised")

    def refresh_token_if_need_it(self):
        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            print(f"refresh token <{self.name}>")
            self.credentials.refresh(Request())

    def upload(self, file_path, name_on_drive):
        self.refresh_token_if_need_it()
        file_meta = {"name": name_on_drive}
        file_media = MediaFileUpload(file_path, mimetype='application/octet-stream')

        print(f"uploading {file_path} as <{name_on_drive}>")
        response = self.service.files().create(
            body=file_meta, media_body=file_media, fields="id, sha256Checksum").execute()

        print(response)

        # Checking checksum
        sha256 = hashlib.sha256()

        # Calc local checksum
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(GoogleDriveAdapter.BUF_SIZE)
                if not data:
                    break
                sha256.update(data)

        # Compare Checksums
        if sha256.hexdigest() != response["sha256Checksum"]:
            raise RuntimeError("Uploading failed. invalid checksum")
        else:
            print("Uploaded successfully")
