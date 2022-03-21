from typing import Optional

import jwt
from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments

from . import interfaces, errors
from .dataclasses import Chat, User, ChatsMembers, ChatMessage

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    login: str
    password: str
    id: Optional[int]


class ChatInfo(DTO):
    creator_id: int
    name: str
    description: str
    id: Optional[int]


class ChatInfoForChange(DTO):
    creator_id: int
    name: str = None
    description: str = None
    id: int = None


class ChatMessageInfo(DTO):
    user_id: int
    chat_id: int
    text: str
    id: Optional[int]


class ChatsMembersInfo(DTO):
    chat_id: int
    user_id: int
    id: Optional[int]


class ChatsMembersInfoForChange(DTO):
    chat_id: int
    user_id: int
    id: Optional[int] = None


@component
class Users:
    user_repo: interfaces.UserRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        new_user = user_info.create_obj(User)
        self.user_repo.add(new_user)
        token = jwt.encode({
            'sub': new_user.id,
            'login': new_user.login,
            'name': new_user.login,
            'group': 'User'
        }, 'secret_jwt', algorithm='HS256')

        return token

    @join_point
    @validate_arguments
    def get_info(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception

        return user


@component
class Chats:
    user_repo: interfaces.UserRepo
    chat_repo: interfaces.ChatRepo
    chat_members_repo: interfaces.ChatsMembersRepo
    chat_message_repo: interfaces.ChatMessageRepo

    def user_check(self, user_id: int):
        if self.user_repo.get_by_id(user_id):
            return True

        raise errors.NoUser(id=user_id)

    def chat_check(self, chat_id: int):
        try:
            user, chat = self.chat_repo.get_by_id(chat_id)
        except TypeError:
            raise errors.NoChat(id=chat_id)

        return user, chat

    @staticmethod
    def is_chat_creator(chat: Chat, user_id: int):
        if chat.creator_id != user_id:
            raise errors.NoCreator(id=user_id)

    def is_chat_participant(self, user_id: int, chat_id: int):
        chat_members = self.chat_members_repo.get_by_chat_id(chat_id)
        if user_id in [chat_member.id for chat_member in chat_members]:
            return True

        raise errors.NoUserInChat(id=user_id)

    @join_point
    @validate_with_dto
    def add_user_to_chat_implementation(self, chat_member_info: ChatsMembersInfo):
        new_row = chat_member_info.create_obj(ChatsMembers)
        self.chat_members_repo.add(new_row)

    @join_point
    @validate_with_dto
    def update_chat_implementation(self, chat_info: ChatInfoForChange):
        user, chat = self.chat_check(chat_info.id)
        self.is_chat_creator(chat, chat_info.creator_id)

        if chat_info.name is None:
            chat_info.name = chat.name
        if chat_info.description is None:
            chat_info.description = chat.description

        chat_info.populate_obj(chat)

    @join_point
    @validate_arguments
    def get_info_chat(self, user_id: int, chat_id: int):
        chat = self.chat_repo.get_by_id(chat_id)
        if self.chat_check(chat_id) and self.is_chat_participant(user_id, chat_id):
            return chat

    @join_point
    @validate_arguments
    def get_users(self, user_id: int, chat_id: int):
        if self.is_chat_participant(chat_id, user_id):
            users = self.chat_members_repo.get_by_chat_id(chat_id)
            return users

    @join_point
    @validate_arguments
    def get_message(self, user_id: int, chat_id: int):
        if self.is_chat_participant(user_id, chat_id):
            message = self.chat_message_repo.get_by_chat_id(chat_id)
            return message

    @join_point
    @validate_with_dto
    def add_chat(self, chat_info: ChatInfo):
        new_chat = chat_info.create_obj(Chat)
        chat_id = self.chat_repo.add(new_chat)
        new_row = ChatsMembersInfo(chat_id=chat_id, user_id=chat_info.creator_id)
        self.add_user_to_chat_implementation(**new_row.dict())

    @join_point
    @validate_arguments
    def update_chat(self, user_id: int, chat_id: int, **kwargs):
        modified_chat_info = ChatInfoForChange(id=chat_id, creator_id=user_id, **kwargs)
        self.update_chat_implementation(**modified_chat_info.dict())

    @join_point
    @validate_arguments
    def remove_chat(self,  user_id: int, chat_id: int):
        user, chat = self.chat_check(chat_id)
        self.is_chat_creator(chat, user_id)
        self.chat_repo.remove(chat)

    @join_point
    @validate_arguments
    def add_user_to_chat(self, user_id: int, chat_id: int, new_user_id: int):
        user, chat = self.chat_check(chat_id)
        self.is_chat_creator(chat, user_id)

        new_row = ChatsMembersInfo(chat_id=chat_id, user_id=new_user_id)
        self.add_user_to_chat_implementation(**new_row.dict())

    @join_point
    @validate_with_dto
    def send_message(self, message_info: ChatMessageInfo):
        self.chat_check(message_info.chat_id)
        self.is_chat_participant(message_info.user_id, message_info.chat_id)

        new_message = message_info.create_obj(ChatMessage)
        self.chat_message_repo.add(new_message)

    @join_point
    @validate_arguments
    def get_chat_messages(self, user_id: int, chat_id: int):
        self.is_chat_participant(user_id, chat_id)
        messages = self.chat_message_repo.get_by_chat_id(chat_id)

        return messages
