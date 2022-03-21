from classic.app.errors import AppError


class NoUser(AppError):
    msg_template = "No user with id '{id}'"
    code = 'chat.no_user'


class NoChat(AppError):
    msg_template = "No chat with id '{id}'"
    code = 'chat.no_chat'


class NoCreator(AppError):
    msg_template = "User with id '{id}' is not creator of this chat"
    code = 'chat.no_creator'


class NoUserInChat(AppError):
    msg_template = "User with id '{id}' is not in this chat"
    code = 'chat.no_user_in_chat'
