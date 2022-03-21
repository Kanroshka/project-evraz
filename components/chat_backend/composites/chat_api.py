from classic.sql_storage import TransactionContext
from sqlalchemy import create_engine

from chat_backend.adapters import chat_api, database
from chat_backend.application import services
from sqlalchemy.orm import sessionmaker


class Settings:
    db = database.Settings()
    chat_api = chat_api.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    user_repo = database.repositories.UserRepo(context=context)
    chat_repo = database.repositories.ChatRepo(context=context)
    chats_members_repo = database.repositories.ChatsMembersRepo(context=context)
    messages_repo = database.repositories.ChatMessageRepo(context=context)


class Application:
    is_dev_mode = Settings.chat_api.IS_DEV_MODE
    user = services.Users(
        user_repo=DB.user_repo
    )
    chat = services.Chats(
        user_repo=DB.user_repo,
        chat_repo=DB.chat_repo,
        chat_members_repo=DB.chats_members_repo,
        chat_message_repo=DB.messages_repo
    )


class Aspects:
    services.join_points.join(DB.context)
    chat_api.join_points.join(DB.context)


app = chat_api.create_app(
    user=Application.user,
    is_dev_mode=Application.is_dev_mode,
    chat=Application.chat,
)

if __name__ == "__main__":
    from wsgiref import simple_server

    with simple_server.make_server('', 8009, app=app) as server:
        server.serve_forever()

