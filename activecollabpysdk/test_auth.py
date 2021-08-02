import os
from dotenv import load_dotenv
import unittest
import json


from cloud import Cloud
from token_sdk import Token
from client import Client


class Test_Login(unittest.TestCase):
    
    def test_login_success(self) -> None:

        load_dotenv()
        my_email = os.getenv('AC_EMAIL')        # str
        my_password = os.getenv('AC_PASSWORD')  # str
        my_ac_url = os.getenv('AC_ACCOUNT_URL') # str
        my_account_id = os.getenv('AC_ACCOUNT_ID') # int

        # Check parameters passed are accurate
        if type(my_account_id) == str:
            my_account_id = int(my_account_id)
        else:
            raise ValueError("Empty account ID")
        if my_email and my_password:
            my_organization = 'My Organization Inc'
            my_app = 'My Dummy App'

            my_cloud = Cloud(my_organization, my_app, my_email, my_password)
        else:
            raise AttributeError('Password and email are empty')

        # Test Authentication
        self.assertTrue(my_cloud.accounts, "Accounts is empty")
        self.assertTrue(my_account_id in my_cloud.accounts)
        self.assertEqual(my_cloud.accounts[my_account_id]['url'], my_ac_url, 'Wrong URL returned')
        self.assertEqual(my_cloud.accounts[my_account_id]['class'], 'FeatherApplicationInstance', 'Wrong application type returned')

        # Testing issue a token
        my_token = my_cloud.issue_token(my_account_id)
        self.assertTrue(type(my_token) == Token)

        # Enable requests from ActiveCollab
        client = Client(my_token)
        
        # Test we can request from ActiveCollab
        response = client.get('info')
        info = {
            "application": "ActiveCollab",
            "version": "7.2.31"
        }
        self.assertEqual(response.json(), info)

if __name__ == '__main__':
    unittest.main()