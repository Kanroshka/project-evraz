from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User, Chat, ChatsMembers, ChatMessage


class UserRepo(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        ...

    @abstractmethod
    def add(self, user: User):
        ...


class ChatRepo(ABC):

    @abstractmethod
    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        ...

    @abstractmethod
    def add(self, chat: Chat):
        ...

    @abstractmethod
    def remove(self, chat: Chat):
        ...


class ChatsMembersRepo(ABC):

    @abstractmethod
    def get_by_chat_id(self, chat_id: int) -> Optional[List[User]]:
        ...

    @abstractmethod
    def add(self, chats_members: ChatsMembers):
        ...


class ChatMessageRepo(ABC):

    @abstractmethod
    def get_by_chat_id(self, chat_id: int) -> Optional[List[ChatMessage]]:
        ...

    @abstractmethod
    def add(self, user: ChatMessage):
        ...
