import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rest_framework.response import Response


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials():
    creds = None
    redirect_uri = "http://localhost:64011/"
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES, redirect_uri)
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())
    return creds


def build_service():
    global service
    user_creds = get_credentials()
    service = build("calendar", "v3", credentials=user_creds)  
    
    return service

def trigger_signin():

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    credentials = flow.run_local_server(port=64011)


def create_event(event_content):
    
    try:
        
        service = build_service()
        calendars = service.calendarList().list().execute()
        primary_calendar_id = calendars['items'][0]['id']
        calendar_info = service.calendars().get(calendarId=primary_calendar_id).execute()
        timezone = calendar_info['timeZone']
        print(calendars)
        
        event_content['start']['timeZone'] = timezone
        event_content['end']['timeZone'] = timezone

        if event_content['conferenceData']['createRequest']['requestId'] != '':
        # Create the event with the link
            event = service.events().insert(calendarId=primary_calendar_id, body=event_content, conferenceDataVersion=1).execute()
        else:
        # Skip creating the link
            event = service.events().insert(calendarId=primary_calendar_id, body=event_content, conferenceDataVersion=0).execute()

        print(f"Event created {event.get('htmlLink')}")
        return Response(event.get('htmlLink'))


        # now = dt.datetime.now().isoformat() + "Z"
        # event_result = service.events().list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime").execute()
        # events = event_result.get("items", [])
        
        # if not events:
        #     print("No upcoming events found!")
        #     return
        
        # for event in events:
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     print(start, event["summary"])

    except HttpError as error:
        print("An error occured: ", error)
