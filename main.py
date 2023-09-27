from __future__ import print_function

from GoogleDriveAdapter import GoogleDriveAdapter

# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']

if __name__ == '__main__':
    adapter = GoogleDriveAdapter("maximon2006")
    adapter.upload(r"C:\Users\maxim\Documents\Ава.jpg", "Test")
