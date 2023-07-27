from requests import post
from exceptions import AuthenticationError, InvalidResponse


class Cloud:
    """
    A class that handles authentication and interaction with the Active Collab Cloud API.

    Attributes:
        email_address (str): The email address of the user.
        password (str): The password of the user.
        your_org_name (str): The name of your organization.
        your_app_name (str): The name of your application.
        accounts (dict): A dictionary of all Feather accounts associated with the user.
        all_accounts (list): A list of all accounts associated with the user.
        user (dict): A dictionary of user information.
        intent (str): The user's intent.
    """

    def __init__(self, email_address, password, your_org_name, your_app_name):
        """
        Initializes a new instance of the Cloud class.

        Args:
            email_address (str): The email address of the user.
            password (str): The password of the user.
            your_org_name (str): The name of your organization.
            your_app_name (str): The name of your application.
        """
        self.email_address = email_address
        self.password = password
        self.your_org_name = your_org_name
        self.your_app_name = your_app_name
        self.accounts = {}
        self.all_accounts = []
        self.user = {}
        self.intent = ""

    def get_accounts(self):
        """
        Returns a list of all Feather accounts associated with the user.

        Returns:
            list: A list of dictionaries representing the Feather accounts.
        """
        self._load_accounts_and_user()
        return list(self.accounts.values())

    def get_all_accounts(self):
        """
        Returns a list of all accounts associated with the user.

        Returns:
            list: A list of dictionaries representing the accounts.
        """
        self._load_accounts_and_user()
        return self.all_accounts

    def get_user(self):
        """
        Returns user information.

        Returns:
            dict: A dictionary representing the user information.
        """
        self._load_accounts_and_user()
        return self.user

    def get_intent(self):
        """
        Returns the user's intent.

        Returns:
            str: The user's intent.
        """
        self._load_accounts_and_user()
        return self.intent

    def issue_token(self, account_id):
        """
        Issues an authentication token for the specified account.

        Args:
            account_id (int): The ID of the account to issue a token for.

        Returns:
            str: An authentication token.
        """
        if not isinstance(account_id, int):
            raise ValueError('Account ID must be an integer')
        self._load_accounts_and_user()
        if account_id not in self.accounts:
            raise ValueError(f"Account #{account_id} not loaded")
        response = post(f"https://app.activecollab.com/{account_id}/api/v1/issue-token-intent", data={
            'client_vendor': self.your_org_name,
            'client_name': self.your_app_name,
            'intent': self.intent
        })
        if response.status_code == 200:
            return f"{response.json().get('token_type')} {response.json().get('access_token')}"
        else:
            raise AuthenticationError('Invalid response')

    def _load_accounts_and_user(self):
        """
        Loads account and user details from Active Collab ID.
        """
        if not self.accounts:
            response = post('https://my.activecollab.com/api/v1/external/login', data={
                'email': self.email_address,
                'password': self.password
            })
            if response.status_code == 200:
                result = response.json()
                if not result.get('is_ok'):
                    raise InvalidResponse(result.get('message'))
                self.accounts = {
                    int(account.get('name')): {
                        'id': int(account.get('name')),
                        'name': account.get('display_name'),
                        'url': account.get('url')
                    } for account in result.get('accounts', []) if account.get('class') in
                    ['FeatherApplicationInstance', r'ActiveCollab\Shepherd\Model\Account\ActiveCollab\FeatherAccount']}
                self.all_accounts = result.get('accounts', [])
                self.intent = result.get('user', {}).get('intent', '')
                self.user = result.get('user', {})
                self.user.pop('intent', None)
            else:
                raise AuthenticationError('Invalid response')
