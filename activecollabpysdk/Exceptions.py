from requests.exceptions import HTTPError


class EmptyArgumentError(ValueError):
    pass


class InvalidArgumentError(ValueError):
    pass


class AuthenticationError(ValueError):
    pass


class InvalidResponse(HTTPError):
    pass
