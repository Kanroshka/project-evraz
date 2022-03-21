from typing import List, Optional, Tuple

from sqlalchemy import select

from classic.components import component
from classic.sql_storage import BaseRepository

from chat_backend.application import interfaces
from chat_backend.application.dataclasses import User, Chat, ChatsMembers, ChatMessage


@component
class UserRepo(BaseRepository, interfaces.UserRepo):
    def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, user: User):
        self.session.add(user)
        self.session.flush()


@component
class ChatRepo(BaseRepository, interfaces.ChatRepo):
    def get_by_id(self, chat_id: int) -> Optional[Tuple[User, Chat]]:
        query = self.session.query(User, Chat).join(User, Chat.creator_id == User.id).where(Chat.id == chat_id)
        return query.one_or_none()

    def add(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()
        self.session.refresh(chat)
        return chat.id

    def remove(self, chat: Chat):
        [self.session.delete(item) for item in self.session.query(ChatsMembers).where(
            ChatsMembers.chat_id == chat.id).all()]

        self.session.delete(chat)
        self.session.flush()


@component
class ChatsMembersRepo(BaseRepository, interfaces.ChatsMembersRepo):
    def get_by_chat_id(self, chat_id: int) -> Optional[List[User]]:
        users = self.session.query(User).join(
            ChatsMembers, User.id == ChatsMembers.user_id).where(ChatsMembers.chat_id == chat_id)
        return users.all()

    def add(self, chats_members: ChatsMembers):
        self.session.add(chats_members)
        self.session.flush()


@component
class ChatMessageRepo(BaseRepository, interfaces.ChatMessageRepo):
    def get_by_chat_id(self, chat_id: int) -> Optional[List[ChatMessage]]:
        query = select(ChatMessage).where(ChatMessage.chat_id == chat_id)
        return self.session.execute(query).scalars().all()

    def add(self, message: ChatMessage):
        self.session.add(message)
        self.session.flush()
