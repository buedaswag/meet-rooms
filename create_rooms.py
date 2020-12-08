'''
How this code works

the slack bot adds users to groups, then with the google api we create a calendar event with the names of the people, then get the meet links for those events and send that to the slack group

on the event object, there should be a goodle meet link

https://api.slack.com/apps/A0178B5RP8D/general
'''
import os
import datetime

from gcsa.google_calendar import GoogleCalendar

# The calendar that will create the events with rooms
CALENDAR_OWNER = os.environ('CALENDAR_OWNER')
CALENDAR_ID = os.environ('CALENDAR_ID')


def _get_start_and_end():
    start = datetime.datetime.now()
    length = datetime.timedelta(minutes=30)
    end = start + length
    string_start = start.isoformat(timespec='seconds')
    string_end = end.isoformat(timespec='seconds')
    return string_start, string_end


def _extract_name(email):
    return email.split('@')[0]


def make_event(attendees, title=False, start_now=True):
    if not start_now:
        raise NotImplementedError('Lazyness is bliss')
    else:
        start, end = _get_start_and_end()
    if not title:
        'Chat with ' + ' '.join([_extract_name(email) for email in attendees])
    event = {}
    event['summary'] = title
    event['descripiton'] = title
    event['start'] = {
        'dateTime': start,
        'timeZone': 'Europe/Lisbon'
    }
    event['end'] = {
        'dateTime': end,
        'timeZone': 'Europe/Lisbon'
    }
    event['attendees'] = []
    for attendee in attendees:
        event['attendees'].append({'email': attendee})
    return event


# SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar = GoogleCalendar(
    CALENDAR_OWNER, credentials_path='client_secret.json')
service = calendar.service

event = make_event(
    attendees=['sam@lisbondatascience.org', 'pedro@lisbondatascience.org'],
    title='Beery test event'
)
event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
