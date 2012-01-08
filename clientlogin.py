import requests
import re
from requests.exceptions import RequestException

class AuthException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class ParseException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class Authenticator(object):

    @staticmethod
    def generate_token(email, password, source,
                       account_type='GOOGLE', service='ac2dm'):

        """Returns an auth token for the supplied service."""

        base_url = 'https://www.google.com/accounts/ClientLogin'

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

        payload = {
            'Email': email,
            'Passwd': password,
            'source': source,
            'accountType': account_type,
            'service': service,
        }

        try:
            response = requests.post(base_url, data=payload, headers=headers)
        except(RequestException):
            raise

        if response.status_code is 200:
            match = re.search('Auth=(\S+)', response.content)
            try:
                return match.group(0)
            except(AttributeError):
                raise ParseException('Parsing Auth token failed')
        else:
            raise AuthException('Service returned %d' % (response.status_code,))
