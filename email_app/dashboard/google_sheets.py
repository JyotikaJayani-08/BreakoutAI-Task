# dashboard/google_sheets.py
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.conf import settings

# Scopes required for Google Sheets access
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_google_flow():
    flow = google_auth_oauthlib.flow.Flow.from_client_config({
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }, scopes=SCOPES)
    flow.redirect_uri = settings.OAUTH_REDIRECT_URI
    return flow

def get_google_sheets_data(credentials, spreadsheet_id, range_name):
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values
