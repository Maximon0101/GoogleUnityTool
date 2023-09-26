class GoogleDriveAdapter:
    SCOPES = ['https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file']

    def __init__(self, name):
        self.name = name
        self.credentials = None
        secret_path = f"secrets/{name}"