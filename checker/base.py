"""Base checker"""
import os
from g_service import calendar


class Checker(object):
    """Checker base"""
    def __init__(self, creds_filename):
        """Base checker"""
        super().__init__()
        self._creds_filename = creds_filename
        self._calendar_service = calendar.Calendar(
            creds_filename=self._creds_filename
        )

    def do_check(self):
        """Do check logic"""
        raise NotImplementedError()

    def check(self):
        """Check logic"""
        self.do_check()
        self.mark_reminder()

    def get_date(self):
        """Get the date of reminder
        :rtype datetime.datetime
        """
        raise NotImplementedError()

    def get_summary(self):
        """Get the summary
        :rtype str
        """
        raise NotImplementedError()

    def mark_reminder(self):
        """Mark the reminder in google calendar"""
        summary = self.get_summary()
        date = self.get_date()
        if summary is not None and date is not None:
            self._calendar_service.insert_event(
                summary=summary, start=date, end=date
            )
            print("Marked reminder on {date} about {summary}".format(
                date=date, summary=summary
            ))
