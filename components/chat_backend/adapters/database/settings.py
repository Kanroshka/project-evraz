from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = 'sqlite:////home/kanroshka/PycharmProjects/project/components/chat.bd'
