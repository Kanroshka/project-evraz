from datetime import datetime

import pytest
from chat_backend.application import dataclasses


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(
        login='login1',
        password='password1',
        id=1
    )


@pytest.fixture(scope='function')
def chat():
    return dataclasses.Chat(
        name='Title1',
        description='description1',
        creator_id=1,
        id=1,
    )


@pytest.fixture(scope='function')
def chats_members():
    return dataclasses.ChatsMembers(
        chat_id=1,
        user_id=1,
        id=1
    )


@pytest.fixture(scope='function')
def chat_message():
    return dataclasses.ChatMessage(
        chat_id=1,
        user_id=1,
        text='my msg',
        id=1,
    )
