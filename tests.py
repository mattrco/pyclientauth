# Copyright 2012 Matt Cottingham
# Licensed under the Apache License, Version 2.0

import unittest2 as unittest
import requests
from mock import patch
from requests.exceptions import RequestException
from clientlogin import Authenticator
from clientlogin import AuthException
from clientlogin import ParseException


@patch.object(requests, 'post')
class AuthenticatorExceptionTests(unittest.TestCase):

    def test_requests_raise(self, post):

        """Verify that requests exceptions are raised to caller."""

        with self.assertRaises(RequestException):
            post.side_effect = RequestException
            Authenticator.generate_token('mail@example.com','password','tag')

    def test_auth_exception(self, post):

        """Verify that response 403 raises AuthException."""

        with self.assertRaises(AuthException):
            post.return_value.status_code = 403
            Authenticator.generate_token('mail@example.com','password','tag')

    def test_parse_exception(self, post):

        """
        Verify that a ParseException is raised if the response body doesn't
        match the expected format.
        """

        with self.assertRaises(ParseException):
            post.return_value.status_code = 200
            post.return_value.content = 'loremipsum'
            Authenticator.generate_token('mail@example.com','password','tag')


if __name__ == '__main__':
    unittest.main()
