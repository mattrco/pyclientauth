import unittest2 as unittest
import requests
from mock import patch
from requests.exceptions import RequestException
from clientlogin import Authenticator
from clientlogin import AuthException
from clientlogin import ParseException

class AuthenticatorExceptionTests(unittest.TestCase):

    def test_requests_raise(self):

        """Verify that requests exceptions are raised to caller."""

        with patch.object(requests, 'post') as mock_method:
            with self.assertRaises(RequestException):
                mock_method.side_effect = RequestException
                Authenticator.generate_token('mail@example.com','password','tag')

    def test_auth_exception(self):

        """Verify that response 403 raises AuthException."""

        with patch.object(requests, 'post') as mock_method:
            with self.assertRaises(AuthException):
                mock_method.return_value.status_code = 403
                Authenticator.generate_token('mail@example.com','password','tag')

    def test_parse_exception(self):

        """
        Verify that a ParseException is raised if the response body doesn't
        match the expected format.
        """

        with patch.object(requests, 'post') as mock_method:
            with self.assertRaises(ParseException):
                mock_method.return_value.status_code = 200
                mock_method.return_value.content = 'loremipsum'
                Authenticator.generate_token('mail@example.com','password','tag')


if __name__ == '__main__':
    unittest.main()
