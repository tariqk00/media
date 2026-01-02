import drive_mcp

def list_plaud_files():
    folder_id = drive_mcp.get_or_create_folder("Filing Cabinet/Plaud")
    print(f"Checking Folder ID: {folder_id}")
    
    service = drive_mcp.get_drive_service()
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name, createdTime)').execute()
    files = results.get('files', [])
    
    if not files:
        print("No files found in folder.")
    else:
        print("Files found:")
        for file in files:
            print(f"- {file['name']} (ID: {file['id']}, Created: {file['createdTime']})")

if __name__ == "__main__":
    list_plaud_files()
