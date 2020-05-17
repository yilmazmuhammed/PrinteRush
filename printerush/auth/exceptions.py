class RegisterException(Exception):
    pass


class EmailAlreadyExist(RegisterException):
    pass


class UsernameAlreadyExist(RegisterException):
    pass


class ThereIsNotWebUser(Exception):
    pass

