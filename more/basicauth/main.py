import binascii
import base64

from morepath import (Identity, NO_IDENTITY)
from morepath.compat import bytes_


class BasicAuthIdentityPolicy(object):
    """Identity policy that uses HTTP Basic Authentication."""

    def __init__(self, realm='Realm'):
        self.realm = realm

    def identify(self, request):
        """Establish claimed identity using request.

        :param request: Request to extract identity information from.
        :type request: :class:`morepath.Request`.
        :return: :class:`morepath.Identity` instance.
        """
        try:
            authorization = request.authorization
        except ValueError:
            return NO_IDENTITY
        if authorization is None:
            return NO_IDENTITY
        authtype, params = authorization
        auth = parse_basic_auth(authtype, params)
        if auth is None:
            return NO_IDENTITY
        return Identity(userid=auth.username, password=auth.password)

    def remember(self, response, request, identity):
        """Remember identity on response.

        This is a no-op for basic auth, as the browser re-identifies
        upon each request in that case.

        :param response: response object on which to store identity.
        :type response: :class:`morepath.Response`
        :param request: request object.
        :type request: :class:`morepath.Request`
        :param identity: identity to remember.
        :type identity: :class:`morepath.Identity`
        """

    def forget(self, response, request):
        """Forget identity on response.

        This causes the browser to issue a basic authentication
        dialog.  Warning: for basic auth, the browser in fact does not
        forget the information even if ``forget`` is called.

        :param response: response object on which to forget identity.
        :type response: :class:`morepath.Response`
        :param request: request object.
        :type request: :class:`morepath.Request`

        """
        response.headers.add('WWW-Authenticate',
                             'Basic realm="%s"' % self.realm)


class BasicAuthInfo(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password


# code taken from
# pyramid.authentication.BasicAuthenticationPolicy._get_credentials
def parse_basic_auth(authtype, params):
    # try:
    #     authtype, params = parse_auth(value)
    # except ValueError:
    #     return None

    if authtype != 'Basic':
        return None
    try:
        authbytes = b64decode(params.strip())
    except (TypeError, binascii.Error):  # can't decode
        return None

    # try utf-8 first, then latin-1; see discussion in
    # https://github.com/Pylons/pyramid/issues/898
    try:
        auth = authbytes.decode('utf-8')
    except UnicodeDecodeError:
        # might get nonsense but normally not get decode error
        auth = authbytes.decode('latin-1')

    try:
        username, password = auth.split(':', 1)
    except ValueError:  # not enough values to unpack
        return None

    return BasicAuthInfo(username, password)


def b64decode(v):
    return base64.b64decode(bytes_(v))
