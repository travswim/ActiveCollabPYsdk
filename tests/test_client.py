from io import BufferedReader
import unittest
from unittest.mock import patch, Mock
import configparser

# from mock import patch
from requests.exceptions import HTTPError

from Exceptions import EmptyArgumentError, \
    InvalidArgumentError
from token_sdk import Token
from client import Client


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

    # Prepare files
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

    # Info & get
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

    @patch('activecollabpysdk.client.requests.post')
    def test_post(self, mock_info):
        mock_info.return_value.status_code = 201
        mock_info.return_value.json.return_value = 'mock response'
        c = self._test_prepare_client()

        url = 'https://www.something.com/'
        data = {'a': 1, 'b': 2}

        _ = c.post(url, data)

        mock_info.assert_called_once_with(
            url='https://www.something.com/api/v1/',
            headers={'X-Angie-AuthApiToken': 'abc'},
            files={},
            json=data
        )

    @patch('activecollabpysdk.client.requests.put')
    def test_put(self, mock_info):
        mock_info.return_value.status_code = 201
        mock_info.return_value.json.return_value = 'mock response'
        c = self._test_prepare_client()

        url = 'https://www.something.com/'
        data = {'a': 1, 'b': 2}

        _ = c.put(url, data)
        # self.assertEqual(actual, 'mock response')
        mock_info.assert_called_once_with(
            url='https://www.something.com/api/v1/',
            headers={'X-Angie-AuthApiToken': 'abc'},
            json=data
        )

    @patch('activecollabpysdk.client.requests.delete')
    def test_delete(self, mock_info):
        mock_info.return_value.status_code = 201
        mock_info.return_value.json.return_value = 'mock response'
        c = self._test_prepare_client()

        url = 'https://www.something.com/'

        _ = c.delete(url)
        # self.assertEqual(actual, 'mock response')
        mock_info.assert_called_once_with(
            url='https://www.something.com/api/v1/',
            headers={'X-Angie-AuthApiToken': 'abc'}
        )

    @patch('activecollabpysdk.client.requests.post')
    def test_post_fail(self, mock_info):
        mock_info.side_effect = HTTPError(
            Mock(return_value={'status_code': 500}), 'error')
        c = self._test_prepare_client()

        url = 'https://www.something.com/'
        data = {'a': 1, 'b': 2}

        with self.assertRaises(SystemExit):
            c.post(url, data)

        mock_info.assert_called_once_with(
            url='https://www.something.com/api/v1/',
            headers={'X-Angie-AuthApiToken': 'abc'},
            json=data,
            files={}
        )

    @patch('activecollabpysdk.client.requests.put')
    def test_put_fail(self, mock_info):
        mock_info.side_effect = HTTPError(
            Mock(return_value={'status_code': 500}), 'error')
        c = self._test_prepare_client()

        url = 'https://www.something.com/'
        data = {'a': 1, 'b': 2}

        with self.assertRaises(SystemExit):
            c.put(url, data)

        mock_info.assert_called_once_with(
            url='https://www.something.com/api/v1/',
            headers={'X-Angie-AuthApiToken': 'abc'},
            json=data
        )

    @patch('activecollabpysdk.client.requests.delete')
    def test_delete_fail(self, mock_info):
        mock_info.side_effect = HTTPError(
            Mock(return_value={'status_code': 500}), 'error')
        c = self._test_prepare_client()

        url = 'https://www.something.com/'

        with self.assertRaises(SystemExit):
            c.delete(url)

        mock_info.assert_called_once_with(
            url='https://www.something.com/api/v1/',
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
