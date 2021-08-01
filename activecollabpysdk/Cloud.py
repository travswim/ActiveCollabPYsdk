from token_sdk import Token
from authenticator import Authenticator
from Exceptions import AuthenticationError, EmptyArgumentError, InvalidArgumentError, InvalidResponse
import requests

class Cloud(Authenticator):

    def __init__(self, your_org_name: str, your_app_name: str, email_address: str, password: str) -> None:
        super().__init__(your_org_name, your_app_name, email_address, password)
        self.__accounts_and_user_loaded = False
        self.__accounts = {}
        self.__user = {}
        self.__intent = ""
    
    # Getter/setters
    @property
    def accounts_and_user_loaded(self) -> bool:
        return self.__accounts_and_user_loaded

    @accounts_and_user_loaded.setter
    def accounts_and_user_loaded(self, value: bool) -> None:
        self.__accounts_and_user_loaded = value

    @property
    def accounts(self) -> dict:
        if not self.__accounts_and_user_loaded:
            self.__load_accounts_and_users()
        return self.__accounts

    @accounts.setter
    def accounts(self, value) -> None:
        if not value:
            raise InvalidArgumentError("Cannot be an empty value")
        self.__accounts[value['name']] = value

    @property
    def user(self) -> dict[str, str]:
        if not self.__accounts_and_user_loaded:
            self.__load_accounts_and_users()

        return self.__user

    @user.setter
    def user(self, value: dict[str, str]) -> None:
        if not value:
            raise InvalidArgumentError('Cannot be empty value')
        self.__user = value

    @property
    def intent(self) -> str:
        if not self.__accounts_and_user_loaded:
            self.__load_accounts_and_users()
        return self.__intent
    
    @intent.setter
    def intent(self, value: str) -> None:
        if not value:
            raise InvalidArgumentError('Cannot be empty value')
        self.__intent = value

    def issue_token(self, account_ID: int) -> Token:
        """Issues a token for a given account ID

        Args:
            account_ID (int): Account ID of the account to issue a token

        Returns:
            Token: A token object containing both the issued token and url
        """

        if not account_ID:
            raise EmptyArgumentError("Need to provide an account ID (int)")

        intent = self.intent

        if account_ID not in self.accounts:
            raise InvalidArgumentError("Account ID is invalid")
        
        url = 'https://app.activecollab.com/' + str(account_ID) + '/api/v1/issue-token-intent'
        email = self.email_address
        app_name = self.app_name
        intent = self.intent

        try:
            r = requests.post(url, data={'client_vendor': email, 'client_name': app_name, 'intent': intent})
            r.raise_for_status() 

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if not r.json() and 'application/json' not in r.headers['content-type']:
            raise AuthenticationError("Invalid response")
        return self.issueTokenResponseToToken(r, self.accounts[account_ID]['url'])

    def __load_accounts_and_users(self):
        """Loads the account information related to an ActiveCollab user
        """
        
        # We have not loaded the accounts yet
        if not self.accounts_and_user_loaded:
            email = self.email_address
            password = self.password
            
            if not email or not password:
                raise AuthenticationError("Password and email are empty")

            url = 'https://my.activecollab.com/api/v1/external/login'
            data = {
                'email': email,
                'password': password
            }
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }

            # Try post to retrieve an intent and account info
            try:
                r = requests.post(url, json=data, headers=headers)
                r.raise_for_status()  
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            
            # Request JSON received
            if r.json() and r.headers['content-type'] == 'application/json':
                response = r.json()

                # Response Failed
                if not response['is_ok']:
                    # No reason for failure
                    if not response['message']:
                        raise AuthenticationError('No response received')
                    # Resons for failure provided
                    else:
                        raise AuthenticationError(response['message'])
                # Did not get an intent
                elif not response['user'] or not response['user']['intent']:
                    raise AuthenticationError('Failed to generate an intent')
                # We have JSON and an intent
                else:
                    if response['accounts'] or type(response['accounts']) == list:
                        for account in response['accounts']:

                            if account['class'] == 'FeatherApplicationInstance' or account['class'] == 'ActiveCollab\Shepherd\Model\Account\ActiveCollab\FeatherAccount': 
                                self.accounts = account

                    # Success, load user values and set account flag to True
                    self.intent = response['user']['intent']
                    self.user = {'avatar_url': response['user']['avatar_url'], 'first_name': response['user']['first_name'], 'last_name': response['user']['last_name']}
                    self.accounts_and_user_loaded = True
            else:
                content_type = r.headers['content-type']
                http_code = r.status_code
                raise AuthenticationError(f'Invalid response. JSON expected, got {content_type}, status code {http_code}')