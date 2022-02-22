from json import JSONDecodeError
from typing import Literal
from requests.models import Response
from activecollabpysdk.Exceptions import AuthenticationError, EmptyArgumentError
from activecollabpysdk.authenticator import Authenticator

import unittest
from email.utils import parseaddr

class Test_Authenticator(unittest.TestCase):
    """
    Test Authentication class methods

    NOTE: We only need to test the response conent, not the url (url is tested in token_sdk)
    """
    def setUp(self) -> None:
        self.org_name: str = 'my_org'
        self.app_name: str = 'my_app'
        valid_email = parseaddr('abc@abc.com')
        if valid_email[0] == valid_email[1] == '':
            raise ValueError('Not a valid email address')
        self.email_address: str = 'abc@abc.com'         
        self.password: str = 'abc123'
    
    def test_issuetoken_pass(self) -> None:
        auth = self._generate_auth(
            "https://www.something.com", b'{"is_ok":true,"token":"abc"}'
        )

        auth.issueTokenResponseToToken(self.response, self.url)

    def test_issuetoken_fail_is_ok(self) -> None:
        auth = self._generate_auth(
            "https://www.something.com", b'{"is_ok":false,"token":"abc"}'
        )

        with self.assertRaises(AuthenticationError):
            auth.issueTokenResponseToToken(self.response, self.url)

    def test_issuetoken_fail_message(self) -> None:
        auth = self._generate_auth(
            "https://www.something.com", b''
        )

        with self.assertRaises(JSONDecodeError):
            auth.issueTokenResponseToToken(self.response, self.url)


    def _generate_auth(self, url: str, response_content: bytes):
        self.url = url
        self.response = Response()
        self.response.status_code = 200
        self.response._content = response_content
        return Authenticator(
            self.org_name, self.app_name, self.email_address, self.password
        )

if __name__ == '__main__':
    unittest.main()