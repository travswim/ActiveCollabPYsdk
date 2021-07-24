import os
from dotenv import load_dotenv
import unittest
from Token import Token
from activecollabpysdk.Cloud import Cloud
from types import Any

class Test_Login(unittest.TestCase):
    
    
    def test_login_success(self) -> None:

        load_dotenv()

        # url = os.getenv('AC_URL')
        my_email = os.getenv('AC_EMAIL')        # str
        my_password = os.getenv('AC_PASSWORD')  # str
        my_ac_url = os.getenv('AC_ACCOUNT_URL') # str
        
        my_account_id = os.getenv('AC_ACCOUNT_ID') # int

        if type(my_account_id) == str:
            my_account_id = int(Any(my_account_id))
        else:
            raise ValueError("Empty account ID")
        if my_email and my_password:
            my_organization = 'My Organization Inc'
            my_app = 'My Dummy App'

            my_cloud = Cloud(my_organization, my_app, my_email, my_password)
        else:
            raise AttributeError('Password and email are empty')

        self.assertTrue(my_cloud.accounts, "Accounts is empty")
        self.assert_(my_account_id in my_cloud.accounts)
        self.assertEquals(my_cloud.accounts[my_account_id]['url'], my_ac_url, 'Wrong URL returned')
        self.assertEquals(my_cloud.accounts[my_account_id]['class'], 'FeatherApplicationInstance', 'Wrong application type returned')

        # Testing issue a token
        my_token = my_cloud.issue_token(my_account_id)
        self.assertTrue(type(my_token) == Token)
        if type(my_token) == Token:
            print(my_token)
        

        my_token.token

if __name__ == '__main__':
    unittest.main()