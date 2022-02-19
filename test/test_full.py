import configparser
import unittest

from activecollabpysdk.Exceptions import EmptyArgumentError
from activecollabpysdk.cloud import Cloud
from activecollabpysdk.token_sdk import Token
from activecollabpysdk.client import Client


class Test_Login(unittest.TestCase):

    
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
    
    def test_auth_success(self) -> None:

        # Check parameters passed are accurate
        if not self.my_account_id:
            raise ValueError("Empty account ID")
        if not self.my_email or not self.my_password:
            raise AttributeError('Password and email are empty')

        

        my_cloud = Cloud(self.my_organization, self.my_app, self.my_email, self.my_password)
        # Convert account_id to int
        my_account_id = int(self.my_account_id)

        # Test Authentication
        self.assertTrue(my_cloud.accounts, "Accounts is empty")
        self.assertTrue(my_account_id in my_cloud.accounts, "Account ID not found")
        self.assertEqual(my_cloud.accounts[my_account_id]['url'], self.my_url, 'Wrong URL returned')
        self.assertEqual(my_cloud.accounts[my_account_id]['class'], 'FeatherApplicationInstance', 'Wrong application type returned')

        # Testing issuing a token
        my_token = my_cloud.issue_token(my_account_id)
        self.assertTrue(type(my_token) == Token)
        # Enable requests from ActiveCollab
        client = Client(my_token)

        # Test we can request from ActiveCollab
        response = client.get('info')
        self.assertEqual(response.json()['application'], 'ActiveCollab')
        self.assertIsNotNone(response.json()['version'] >= '7.2.66')


if __name__ == '__main__':
    unittest.main()