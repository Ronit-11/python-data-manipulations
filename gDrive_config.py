from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive.file']

creds = None
def credentialsSetup():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    global creds
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('gDrive/token.json'):
        creds = Credentials.from_authorized_user_file('gDrive/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        dirPath = 'gDrive'
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                dirPath +'/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(dirPath + '/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def create_folder(folder_Name):
    """ Create a folder and prints the folder ID
    Returns : Folder Id
    """
    #creds, _ = google.auth.default()

    try:
        
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': folder_Name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
    
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='id').execute()
        print(F'Folder ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None

    def upload_to_folder(folder_id, loc_folder_Name, file_Name, file_Type):
        """Upload a file to the specified folder and prints file ID, folder ID
        Args: Id of the folder
        Returns: ID of the file uploaded
        """
        # creds, _ = google.auth.default()

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_metadata = {
                'name': file_Name,
                'parents': [folder_id]
            }
            media = MediaFileUpload((loc_folder_Name + '/' + file_Name),
                                    mimetype=file_Type, resumable=True)
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                          fields='id').execute()
            print(F'File ID: "{file.get("id")}".')
            return file.get('id')

        except HttpError as error:
            print(F'An error occurred: {error}')
            return None