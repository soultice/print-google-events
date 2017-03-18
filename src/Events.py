from __future__ import print_function
import httplib2
import os

from collections import defaultdict
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

class EventGetter():

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


    def get_results_list(self):
        raise NotImplementedError


    def get_next_events(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        curr = datetime.datetime.utcnow()
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print(now)
        day_delta = curr.replace(hour=23, minute=59)
        day_delta = day_delta + datetime.timedelta(days=4)
        day_delta = day_delta.isoformat() + 'Z'
        print(day_delta)


        cal_event_list = defaultdict(list)
        calendarsResult = service.calendarList().list(
            syncToken=None, minAccessRole=None, maxResults=None,
            showDeleted=None, showHidden=None, pageToken=None
            ).execute()
        for cal in (calendarsResult.get('items', [])):
            eventsResult = service.events().list(
                calendarId=cal['id'], timeMin=now, timeMax = day_delta,
                singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            if not events:
                print('No upcoming events found.')
            for event in events:
                if event['start'].get('date') is not None:
                    day = event['start'].get('date')
                    day = int(day.replace('-', ''))
                else:
                    day = event['start'].get('dateTime')[:10]
                    day = int(day.replace('-', ''))
                start = event['start'].get('dateTime',
                        event['start'].get('date'))
                cal_event_list[day].append(
                        (start[11:], event['summary']))
        return cal_event_list


if __name__ == '__main__':
    this = EventGetter()
    this.get_credentials()
    this.get_next_events()
