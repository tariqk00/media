"""
FastMCP Server implementation for Google Drive.
Exposes tools to Create Folders and Upload Files (Text/Binary).
"""
import os.path
import io
import base64
from typing import Optional, List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from mcp.server.fastmcp import FastMCP

# If modifying these scopes, delete the file config/token_drive.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata.readonly']

mcp = FastMCP("GoogleDrive")

def get_drive_service():
    creds = None
    if os.path.exists('config/token_drive.json'):
        creds = Credentials.from_authorized_user_file('config/token_drive.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('config/token_drive.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

@mcp.tool()
def get_or_create_folder(folder_path: str) -> str:
    """
    Get the ID of a folder path (e.g., 'Filing Cabinet/Plaud').
    Creates the folders if they don't exist.
    """
    service = get_drive_service()
    parts = folder_path.strip('/').split('/')
    parent_id = 'root'
    
    for part in parts:
        query = f"name = '{part}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed = false"
        results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = results.get('files', [])
        
        if not files:
            file_metadata = {
                'name': part,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            parent_id = folder.get('id')
        else:
            parent_id = files[0].get('id')
            
    return parent_id

@mcp.tool()
def upload_file(filename: str, content: str, folder_id: str, mime_type: str = 'text/markdown') -> str:
    """
    Upload a text file (like Markdown) to a specific Google Drive folder.
    """
    service = get_drive_service()
    try:
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        fh = io.BytesIO(content.encode())
        media = MediaIoBaseUpload(fh, mimetype=mime_type, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return f"File ID: {file.get('id')}"
    except HttpError as error:
        return f"An error occurred: {error}"

@mcp.tool()
def upload_binary_file(filename: str, base64_content: str, folder_id: str, mime_type: str = 'application/octet-stream') -> str:
    """
    Upload a binary file (from base64 string) to a specific Google Drive folder.
    """
    service = get_drive_service()
    try:
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        file_content = base64.urlsafe_b64decode(base64_content)
        fh = io.BytesIO(file_content)
        media = MediaIoBaseUpload(fh, mimetype=mime_type, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return f"File ID: {file.get('id')}"
    except HttpError as error:
        return f"An error occurred: {error}"

if __name__ == "__main__":
    mcp.run()
