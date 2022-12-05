import unittest
from activecollabpysdk.Exceptions import InvalidArgumentError
from activecollabpysdk.token_sdk import Token


class Test_Token(unittest.TestCase):

    def test_invalid_token(self):
        self._validate_token_arguments('', 'https://www.activecollab.com')

    def test_invalid_url(self):
        self._validate_token_arguments('abc123', 'example.com')

    def test_invalid_token_url(self):
        self._validate_token_arguments('', 'example.com')

    def test_valid_token_url(self):
        my_token = 'abc123'
        my_url = 'https://www.activecollab.com'

        try:
            token = Token(my_token, my_url)
            self.assertIsInstance(token, Token, "Token object not created")
        except InvalidArgumentError as e:
            self.fail(f'Unexpected argument failure: {e}')

    # Helper function for testing invalid arguments
    def _validate_token_arguments(self, my_token: str, my_url: str):
        with self.assertRaises(InvalidArgumentError):
            Token(my_token, my_url)


if __name__ == '__main__':
    unittest.main()
