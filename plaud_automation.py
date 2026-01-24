"""
Main automation workflow for Plaud.ai.
Orchestrates: Gmail Search -> Content Extraction -> Drive Upload -> Email Archiving.
"""
import datetime
import gmail_mcp
import drive_mcp

def format_date_time(date_str):
    # Example date_str: "Tue, 30 Dec 2025 15:45:00 +0000"
    # We want "YYYY-MM-DD HH:MM"
    try:
        dt = datetime.datetime.strptime(date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def main():
    print("Starting Plaud.ai Automation...")
    
    # 1. Search for emails
    # Calling the functions from the modules directly.
    emails = gmail_mcp.search_plaud_emails()
    
    if not emails or (isinstance(emails, list) and len(emails) > 0 and isinstance(emails[0], str) and "error" in emails[0].lower()):
        print(f"Error or no emails found: {emails}")
        return
    
    if not emails:
        print("No new Plaud.ai emails found.")
        return

    # 2. Get/Create Drive Folder
    folder_id = drive_mcp.get_or_create_folder("Filing Cabinet/Plaud")
    print(f"Target Drive Folder ID: {folder_id}")

    for email in emails:
        print(f"Processing email: {email['subject']} ({email['date']})")
        
        # 3. Get Full Content
        content = gmail_mcp.get_email_content(email['id'])
        
        if "error" in content:
            print(f"Error fetching content for {email['id']}: {content['error']}")
            continue
            
        # 4. Format Title and Filenames
        formatted_date = format_date_time(email['date'])
        title = f"{formatted_date} {email['subject']}"
        markdown_filename = f"{title}.md"
        
        # 5. Create Markdown Content
        md_body = f"# {email['subject']}\n\n"
        md_body += f"**Date:** {email['date']}\n"
        md_body += f"**From:** PLAUD.AI\n\n"
        md_body += "---\n\n"
        md_body += content['body']
        
        # 6. Upload Markdown to Drive
        print(f"Uploading Markdown: {markdown_filename}")
        drive_mcp.upload_file(markdown_filename, md_body, folder_id)
        
        # 7. Handle Attachments
        for att in content['attachments']:
            att_filename = f"{formatted_date} {att['filename']}"
            print(f"Uploading Attachment: {att_filename}")
            att_data = gmail_mcp.download_attachment(email['id'], att['attachmentId'])
            drive_mcp.upload_binary_file(att_filename, att_data, folder_id)
            
        # 8. Archive Email
        print(f"Archiving thread: {email['threadId']}")
        gmail_mcp.archive_email_thread(email['threadId'])

    print("Automation completed successfully.")

if __name__ == "__main__":
    main()
