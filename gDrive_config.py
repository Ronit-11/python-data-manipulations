from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive.file']

creds = None
def credentialsSetup():
    global creds

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
        print(f'An error occurred: {error}')

def create_folder(folder_Name):
    try:
        
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': folder_Name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
    
        file = service.files().create(body=file_metadata, fields='id').execute()
        print(F'Folder ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None

def upload_to_folder(folder_id, loc_folder_Name, file_Name, file_Type):
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

def search(mimeType, fileName):
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q="mimeType='" +mimeType + "'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None

    for file in files:
        if file.get('name') == fileName:
            return file.get("id")

    return None

def dirFilesUploader(dir_Name, file_Mime):
    folder_Mime = 'application/vnd.google-apps.folder'
    folder = None
    
    folder = search(folder_Mime, dir_Name)
    if folder == None:
        folder = create_folder(dir_Name)
    
    directory = os.fsencode(dir_Name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        files = search(file_Mime, filename)
        if files == None:
            upload_to_folder(folder, dir_Name, filename, file_Mime)

def main():
    credentialsSetup()

    xlsx_Mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    dir2_Name = 'Gen_xlsx_files'
    dirFilesUploader(dir2_Name, xlsx_Mime)

    jsonl_Mime = 'application/jsonl'
    dir1_Name = 'jsonl_files'
    dirFilesUploader(dir1_Name, jsonl_Mime)

if __name__ == '__main__':
    main()