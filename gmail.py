"""
CREATED BY B20DCCN728 - MARK LORENZO
------------------------------------------------
Python script to retrieve Gmail messages using the Gmail API.

This script uses the Gmail API to authenticate with a Gmail account, fetch a list of messages, and then retrieves the content of each message. Make sure to set up the necessary API credentials and enable the Gmail API in the Google Cloud Console before running this script.

Requirements:
- Google API client library: Install using `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

Instructions:
1. Enable the Gmail API in the Google Cloud Console.
2. Create API credentials and download the JSON file.
3. Place the JSON file in the same directory as this script.
4. Run the script to authenticate and fetch Gmail messages.

Note: Ensure that you have the necessary permissions to access the Gmail account.

Author: Mark Lorenzo
Date: 2024-02-04
"""
import base64
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_new_message() -> dict:
    """Shows basic usage of the Gmail API. Lists the user's Gmail messages."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build(
            "gmail",
            "v1",
            credentials=creds
        )
        results = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            q="is:unread"
        ).execute()
        messages = results.get("messages", [])
        if not messages:
            return {
                "name": "error",
                "from_name": "",
                "value": "No new messages found!!"
            }
        else:
            mgs = service.users().messages().get(
                userId="me",
                id=messages[0]["id"]
            ).execute()
            email_data = mgs['payload']['headers']
            from_name = ""
            for value in email_data:
                name = value['name']
                if name == "From":
                    from_name = value['value']
                    print("You have new message from " + from_name)

            # Access the body of the message
            if 'parts' in mgs['payload']:
                message_body = mgs['payload']['parts'][0]['body']['data']
            else:
                message_body = mgs['payload']['body']['data']

            # Decode the base64 string
            message_body = base64.urlsafe_b64decode(message_body).decode("utf-8")
            return {
                "name": "success",
                "from_name": from_name,
                "value": message_body
            }

    except HttpError as error:
        return {
            "name": "error",
            "from_name": "",
            "value": f"An error occurred: {error}"
        }