from unittest.mock import Mock

import pytest

from chat_backend.application import interfaces


@pytest.fixture(scope='function')
def user_repo(user):
    user_repo = Mock(interfaces.UserRepo)
    user_repo.get_by_id = Mock(return_value=user)
    user_repo.add = Mock(return_value=user)

    return user_repo


@pytest.fixture(scope='function')
def chat_repo(chat):
    chat_repo = Mock(interfaces.ChatRepo)
    chat_repo.get_by_id = Mock(return_value=chat)
    chat_repo.add = Mock(return_value=chat)
    chat_repo.remove = Mock(return_value=chat)

    return chat_repo


@pytest.fixture(scope='function')
def chat_messages_repo(chat_messages):
    chat_messages_repo = Mock(interfaces.ChatMessageRepo)
    chat_messages_repo.get_by_chat_id = Mock(return_value=chat_messages)
    chat_messages_repo.add = Mock(return_value=chat_messages)

    return chat_messages_repo


@pytest.fixture(scope='function')
def chat_members_repo(chat_members):
    chat_members_repo = Mock(interfaces.ChatsMembersRepo)
    chat_members_repo.get_by_chat_id = Mock(return_value=[chat_members])
    chat_members_repo.add = Mock(return_value=chat_members)

    return chat_members_repo
