from chat_backend.application import services
from classic.http_api import App
from classic.http_auth import Authenticator


from . import controllers, auth


def create_app(
        is_dev_mode: bool,
        user: services.User,
        chat: services.Chat,
) -> App:

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    if is_dev_mode:
        authenticator.set_strategies(auth.jwt_strategy)

    app = App(prefix='/api')

    app.register(controllers.Users(authenticator=authenticator, user=user))
    app.register(controllers.Chats(authenticator=authenticator, chat=chat))

    return app
