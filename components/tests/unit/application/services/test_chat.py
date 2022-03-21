import pytest
from attr import asdict
from chat_backend.application.services import Chats, Users


@pytest.fixture(scope='function')
def service_user(user_repo):
    return Users(user_repo=user_repo)


@pytest.fixture(scope='function')
def service_chat(user_repo, chat_repo, chat_members_repo, chat_message_repo):
    return Chats(user_repo=user_repo, chat_repo=chat_repo, chat_members_repo=chat_members_repo,
                 chat_message_repo=chat_message_repo)


data_user = {
    'login': 'login_1',
    'password': 'password_1',
    'id': 1
}

data_chat = {
    'creator_id': 1,
    'name': 'chat_name_1',
    'description': 'description',
    'id': 1
}

data_chat_update = {
    'creator_id': 1,
    'name': 'chat_new',
    'description': 'description_new',
    'id': 1
}

data_chat_user = {
    'chat_id': 1,
    'user_id': 1,
    'id': 1
}

data_chat_msg = {
    'chat_id': 1,
    'user_id': 1,
    'text': 'my msg',
    'id': 1
}


def test_add_user(service_user):
    service_user.add_user(**data_user)
    service_user.user_repo.add.assert_called_once()


# def test_get_info_chat(service_chat):
#     chat = service_chat.data_message(id=1)
#     assert asdict(chat) == data_chat
#
#
# def test_add_chat_user(service_chat):
#     service_chat.get_by_chat_id(**data_chat_user)
#     service_chat.chat_members_repo.add.assert_called_once()
#
#
# def test_get_chat(service_chat):
#     chat = service_chat.get_chat_by_id(chat_id=1)
#     assert asdict(chat) == data_chat
#
#
# def test_get_user(service_chat):
#     user = service_chat.get_users(user_id=data_user['id_user'])
#     assert asdict(user) == data_user
