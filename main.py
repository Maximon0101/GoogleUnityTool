from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from GoogleDriveAdapter import GoogleDriveAdapter

# If modifying these scopes, delete the file token.json.


        #https://www.googleapis.com/auth/drive.metadata.readonly',
         # 'https://www.googleapis.com/auth/drive.admin.labels.readonly',
          #'https://www.googleapis.com/auth/drive.appdata',
         # ,
          #'https://www.googleapis.com/auth/drive.labels',
          #'https://www.googleapis.com/auth/drive.labels.readonly',
          #'https://www.googleapis.com/auth/drive.admin.labels',
          #'https://www.googleapis.com/auth/docs',
          #'https://www.googleapis.com/auth/drive.photos.readonly',
          #'https://www.googleapis.com/auth/drive.apps.readonly',"""

SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']

          #'https://www.googleapis.com/auth/drive.metadata',
          #'https://www.googleapis.com/auth/drive.metadata.readonly',
          #'https://www.googleapis.com/auth/drive.readonly',
          #'https://www.googleapis.com/auth/drive.scripts',"""

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/maximon2006.secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        file_meta = {'name': 'helloworld.txt'}
        file_media = MediaFileUpload('helloworld.txt', mimetype='plain/text')

        response = service.files().create(body=file_meta, media_body=file_media, fields="id, size, name, sha256Checksum").execute()
        print(response)
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    adapter = GoogleDriveAdapter("maximon2006")

