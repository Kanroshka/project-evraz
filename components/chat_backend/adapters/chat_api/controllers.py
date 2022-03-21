from chat_backend.application import services
from classic.components import component
from classic.http_auth import authenticate, authenticator_needed

from .join_points import join_point


@authenticator_needed
@component
class Users:
    user: services.Users

    @join_point
    def on_post_register(self, request, response):
        response.media = self.user.add_user(**request.media)

    @join_point
    @authenticate
    def on_get_show_info(self, request, response):
        users = self.user.get_info(**request.params)
        response.media = {
            'user_id': users.id,
            'login': users.login,
            'name': users.name
        }


@authenticator_needed
@component
class Chats:
    chat: services.Chats

    @join_point
    @authenticate
    def on_get_show_info(self, request, response):
        user, chat = self.chat.get_info_chat(**request.params)
        response.media = {
            'name': chat.name,
            'description': chat.description,
            'creator_id': chat.creator_id
        }

    @join_point
    @authenticate
    def on_post_add_chat(self, request, response):
        self.chat.add_chat(**request.media)

        response.media = {
            'msg': 'New chat created!'
        }

    @join_point
    @authenticate
    def on_post_update_chat(self, request, response):
        self.chat.update_chat(**request.media)
        response.media = {
            'msg': 'Chat modified!'
        }

    @join_point
    @authenticate
    def on_post_remove_chat(self, request, response):
        self.chat.remove_chat(**request.media)
        response.media = {
            'msg': 'Chat deleted!'
        }

    @join_point
    @authenticate
    def on_post_add_user_to_chat(self, request, response):
        self.chat.add_user_to_chat(**request.media)
        response.media = {
            'msg': 'User added to chat!'
        }

    @join_point
    @authenticate
    def on_post_send_message(self, request, response):
        self.chat.send_message(**request.media)
        response.media = {
            'msg': 'Message sent to chat!'
        }

    @join_point
    @authenticate
    def on_post_show_messages(self, request, response):
        data = self.chat.get_chat_messages(**request.media)
        response.media = [{
                'message_from_user_id': msg.user_id,
                'text': msg.text
            } for msg in data]
