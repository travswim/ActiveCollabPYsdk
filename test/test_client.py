import json
from io import BufferedReader
import unittest
from unittest.mock import patch
import configparser

# from mock import patch
from requests import Response

from activecollabpysdk.Exceptions import EmptyArgumentError, InvalidArgumentError
from activecollabpysdk.token_sdk import Token
from activecollabpysdk.client import Client


# TODO: Hard test (full API request)
# TODO: Soft test (mock responses)
class Test_Client(unittest.TestCase):

    def setUp(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        if not config.sections():
            raise EmptyArgumentError('No sections in config file')

        self.my_email = config['LOGIN']['ACemail']
        self.ac_url = config['LOGIN']['ACurl']
        self.my_password = config['LOGIN']['ACpassword']
        self.my_account_id = config['LOGIN']['ACaccountid']
        self.my_url = config['LOGIN']['ACbaseurl'] + str(self.my_account_id)
        self.my_organization = 'My Organization Inc'
        self.my_app = 'My Dummy App'


    def test_prepare_url(self):
        c = self._test_prepare_client()

        r = c._prepare_url('info')
        self.assertEqual(r, 'https://www.something.com/api/v1/info')

    def test_prepare_url_fail(self):
        c = self._test_prepare_client()
        self.assertRaises(InvalidArgumentError, c._prepare_url, '')

    def test_prepare_files_success(self):
        c = self._test_prepare_client()
        file_path = 'README.md'
        x = c._prepare_files([file_path])
        self.assertIs(type(list(x.values())[0]), BufferedReader)

    def test_prepare_files_fail_filepath(self):
        c = self._test_prepare_client()
        file_path = 'abc.txt'
        with self.assertRaises(FileNotFoundError):
            c._prepare_files([file_path])        

    @patch('activecollabpysdk.client.requests.get')
    def test_info(self, mock_info):
        mock_info.return_value.status_code = 201
        mock_info.return_value.json.return_value = 'mock response'
        c = self._test_prepare_client()
        actual = c.info()
        self.assertEqual(actual, 'mock response')
        mock_info.assert_called_once_with(
            url='https://www.something.com/api/v1/info',
            headers={'X-Angie-AuthApiToken': 'abc'}
        )  

    def _test_prepare_client(self):
        """
        Driver function for testing client files
        """
        t = Token('abc', 'https://www.something.com')
        return Client(t, 1)

    

if __name__ == '__main__':
    unittest.main()