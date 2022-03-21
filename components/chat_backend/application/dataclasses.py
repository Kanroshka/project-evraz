from typing import List, Optional

import attr


@attr.dataclass
class User:
    login: str
    password: str
    id: Optional[int] = None


@attr.dataclass
class Chat:
    name: str
    description: str
    creator_id: User
    id: Optional[int] = None


@attr.dataclass
class ChatsMembers:
    chat_id: Chat
    user_id: User
    id: Optional[int] = None


@attr.dataclass
class ChatMessage:
    user_id: User
    chat_id: Chat
    text: str
    id: Optional[int] = None

