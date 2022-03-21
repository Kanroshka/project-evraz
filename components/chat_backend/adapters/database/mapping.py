from sqlalchemy.orm import registry

from chat_backend.application import dataclasses
from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.Chat, tables.chat)

mapper.map_imperatively(dataclasses.User, tables.user)

mapper.map_imperatively(dataclasses.ChatMessage, tables.chat_message)

mapper.map_imperatively(dataclasses.ChatsMembers, tables.chats_members)

