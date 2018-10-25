"""Authorization for google api"""
from oauth2client import client, file, tools


class Auth(object):
    """Auth handler"""
    def __init__(
        self, scopes, creds_filename='credentials.json',
        token_filename='token.json'
    ):
        """Init"""
        super().__init__()
        self._scopes = scopes
        self._creds_filename = creds_filename
        self._token_filename = token_filename
        self._creds = None

    @property
    def creds(self):
        """Getter for creds"""
        return self._creds

    @property
    def is_authed(self):
        """Check whether already authed."""
        return self._creds is not None

    def auth(self):
        """Do the authorization logic"""
        store = file.Storage(self._token_filename)
        self._creds = store.get()
        if not self._creds or self._creds.invalid:
            flow = client.flow_from_clientsecrets(
                self._creds_filename, self._scopes
            )
            self._creds = tools.run_flow(flow, store)

    @classmethod
    def auth_with_services(
            cls, services, **kwargs
    ):
        """Create the auth instance with the given services."""
        scopes = ''
        for s in services:
            if len(scopes) == 0:
                scopes = s.SCOPE
            else:
                scopes = ' '.join([scopes, s.SCOPE])
        auth_obj = cls(scopes, **kwargs)
        auth_obj.auth()

        return auth_obj
