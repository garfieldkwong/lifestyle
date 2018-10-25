"""Calendar API"""
from . import base


class Calendar(base.BaseHandler):
    """Calendar API handler"""
    SCOPE = 'https://www.googleapis.com/auth/calendar'
    SERVICE_NAME = 'calendar'
    API_VERSION = 'v3'

    def insert_event(self, summary, start, end):
        """Insert an event."""
        event = {
            'summary': summary,
            'start': {
                'date': start.date().isoformat()
            },
            'end': {
                'date': end.date().isoformat()
            },
            'reminders': {
                'useDefault': True
            }
        }
        event = self._service.events().insert(
            calendarId='primary', body=event
        ).execute()
        return event

    def delete_event(self, id):
        """Delete the event by given event ID"""
        self._service.events().delete(
            calendarId='primary', eventId=id
        ).execute()
