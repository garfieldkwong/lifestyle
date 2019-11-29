from . import base


class GMail(base.BaseHandler):
    """Gmail handler"""
    SCOPE = 'https://mail.google.com'
    SERVICE_NAME = 'gmail'
    API_VERSION = 'v1'

    def list_labels(self):
        """List all labels"""
        results = self._service.users().labels().list(
            userId=self.USER_ID
        ).execute()
        return results.get('labels', [])

    def get_message(self, msg_id):
        """Query the specific email message by givin message id"""
        message = self._service.users().messages().get(
            userId=self.USER_ID, id=msg_id
        ).execute()
        return message

    def list_messages(self, query='', labelIds=None):
        """List all message with the given query option."""
        messages = []
        if labelIds is None:
            labelIds = []
        response = self._service.users().messages().list(
            userId=self.USER_ID,
            labelIds=labelIds,
            q=query
        ).execute()

        if 'messages' in response:
            messages.extend(response['messages'])
        return messages

    def mark_as_read(self, msg_id):
        """Mark the message as read"""
        message = self._service.users().messages().modify(
            userId=self.USER_ID,
            id=msg_id,
            body={
                'removeLabelIds': ['UNREAD']
            }
        ).execute()
        return message

    def delete_msg(self, msg_id):
        """Delete message"""
        message = self._service.users().messages().delete(
            userId=self.USER_ID,
            id=msg_id,
        ).execute()
        return message
