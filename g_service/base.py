"""Handler base"""
from googleapiclient import discovery
from httplib2 import Http
from . import auth


class BaseHandler(object):
    """Base handler"""
    SCOPE = None
    SERVICE_NAME = None
    USER_ID = 'me'
    API_VERSION = None

    def __init__(self, auth_obj=None, creds_filename=None):
        """Init"""
        if auth_obj is not None:
            self._auth = auth_obj
        else:
            kwargs = {
                'token_filename': self.SERVICE_NAME + '_token.json'
            }
            if creds_filename is not None:
                kwargs['creds_filename'] = creds_filename
            self._auth = auth.Auth(self.SCOPE, **kwargs)
            self._auth.auth()
        self._service = discovery.build(
            self.SERVICE_NAME, self.API_VERSION,
            http=self._auth.creds.authorize(Http())
        )
