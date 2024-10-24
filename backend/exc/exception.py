from typing import Literal


class UserAlreadyExists(Exception):
    def __init__(self, arg: Literal["name", "username"], value: str):
        self.arg = arg
        self.value = value


class UserNotFound(Exception):
    pass


class IncorrectPassword(Exception):
    pass

class SessionNotFound(Exception):
    pass

class WrongChatUsers(Exception):
    pass

class ChatNotFound(Exception):
    pass