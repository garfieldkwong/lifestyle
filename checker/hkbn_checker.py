"""Checker for hkbn"""
import datetime
import os
import re
from g_service import gmail
from . import base
TARGET_REGEX = re.compile(
    '.*本期應繳賬項.*(\$[0-9]+(\.[0-9]*)?).*'
    '到期繳款日.*([0-9]{4}\/[0-9]{2}\/[0-9]{2}).*'
)

TARGET_LABEL = '賬單/HKBN 賬單'


class Checker(base.Checker):
    """HKBN checker"""
    def __init__(self, creds_filename):
        """Init"""
        super().__init__(creds_filename)
        self._gmail_service = gmail.GMail(
            creds_filename=creds_filename
        )
        self._date = None
        self._summary = None

    def do_check(self):
        """The check logic"""
        # Get the label first.
        labels = self._gmail_service.list_labels()
        target_label_ids = []
        for label in labels:
            if label['name'] == TARGET_LABEL:
                target_label_ids.append(label['id'])

        msg_infos = self._gmail_service.list_messages(
            query='is:unread', labelIds=target_label_ids
        )

        for msg_info in msg_infos:
            msg_data = self._gmail_service.get_message(msg_info['id'])
            matched = TARGET_REGEX.match(msg_data['snippet'])
            if matched is None:
                continue
            money = matched.group(1)
            date = matched.group(3)
            year, month, day = date.split('/')
            self._date = datetime.datetime(
                year=int(year), month=int(month), day=int(day)
            )
            self._summary = ' '.join([TARGET_LABEL, money])

            self._gmail_service.mark_as_read(msg_data['id'])

    def get_date(self):
        """Retrieve the date"""
        return self._date

    def get_summary(self):
        """Retrieve summary"""
        return self._summary
