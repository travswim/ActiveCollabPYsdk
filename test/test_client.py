import imp
import unittest
import configparser

from activecollabpysdk.Exceptions import EmptyArgumentError
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
        t = Token('abc', 'https://www.something.com')
        c = Client(t, 1)
        c.__prepare_url('info')
    


if __name__ == '__main__':
    unittest.main()