from sqlalchemy import (MetaData,
                        Table,
                        Column,
                        Integer,
                        String,
                        ForeignKey,)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('login', String, nullable=True),
    Column('password', String, nullable=True)
)

chat = Table(
    'chat',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('description', String, nullable=False),
    Column('creator_id', ForeignKey('user.id'), nullable=False)
    )

chats_members = Table(
    'chats_members',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('chat_id', ForeignKey('chat.id'), nullable=False),
    Column('user_id', ForeignKey('user.id'), nullable=False)
)

chat_message = Table(
    'chat_message',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user.id'), nullable=False),
    Column('chat_id', ForeignKey('chat.id'), nullable=False),
    Column('text', String, nullable=False)
)
