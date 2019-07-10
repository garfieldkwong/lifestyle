"""Checker for clp bill"""
import datetime
from g_service import gmail
from . import base


class Checker(base.Checker):
    """CLP checker"""
    def __init__(
        self, creds_filename, label, target_regex, datetime_fmt
    ):
        """Init"""
        super().__init__(creds_filename)
        self._gmail_service = gmail.GMail(
            creds_filename=creds_filename
        )
        self._label = label
        self._target_regex = target_regex
        self._date = None
        self._summary = None
        self._datetime_fmt = datetime_fmt

    def do_check(self):
        """The checking logic"""
        # Get the label first
        labels = self._gmail_service.list_labels()
        target_label_ids = []
        for label in labels:
            if label['name'] == self._label:
                target_label_ids.append(label['id'])

        msg_infos = self._gmail_service.list_messages(
            query='is:unread', labelIds=target_label_ids
        )

        for msg_info in msg_infos:
            msg_data = self._gmail_service.get_message(msg_info['id'])
            regex, money_group, date_group = self._target_regex
            matched = regex.match(msg_data['snippet'])
            if matched is None:
                continue
            money = matched.group(money_group)
            date = matched.group(date_group)
            self._date = datetime.datetime.strptime(date, self._datetime_fmt)
            self._summary = ' '.join([self._label, money])

            self._gmail_service.mark_as_read(msg_data['id'])

    def get_date(self):
        """Retrieve the date"""
        return self._date

    def get_summary(self):
        """Retrieve summary"""
        return self._summary