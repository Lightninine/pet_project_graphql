import channels_graphql_ws
import graphene
from django.db.models import Model
from graphene import String
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_auth.decorators import login_required

from core.models import ChatModel, MessageModel
from users.models import CustomUser


class ChatType(DjangoObjectType):
    class Meta:
        model = ChatModel
        fields = "__all__"


class MessageType(DjangoObjectType):
    class Meta:
        model = MessageModel
        fields = "__all__"


class ChatInput(graphene.InputObjectType):
    participants = graphene.List(String)


class CreateChat(graphene.Mutation):
    class Arguments:
        chat_data = ChatInput(required=True)

    chat = graphene.Field(ChatType)

    @staticmethod
    def mutate(root, info, chat_data=None):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged')
        chat_instance = ChatModel.objects.create()
        if chat_data.participants is not None:
            participants_set = [info.context.user]
            for username in chat_data.participants:
                user = CustomUser.objects.get(username=username)
                participants_set.append(user)
            chat_instance.participants.set(participants_set)

        chat_instance.save()
        return CreateChat(chat=chat_instance)


class MessageInput(graphene.InputObjectType):
    message = graphene.String()
    chat = graphene.Int()


class CreateMessage(graphene.Mutation):
    class Arguments:
        message_data = MessageInput(required=True)

    message = graphene.Field(MessageType)

    @staticmethod
    def mutate(root, info, message_data=None):
        author = info.context.user
        if author.is_anonymous:
            raise GraphQLError('You must be logged')
        message = message_data.message
        try:
            chat = ChatModel.objects.get(id=message_data.chat, chat__participants=info.context.user)
        except Model.DoesNotExist:
            raise GraphQLError('Chat does not exist')
        message_instance = MessageModel(
            message=message,
            author=author,
            chat=chat
        )
        message_instance.save()

        OnNewChatMessage.new_chat_message(chat=str(chat.id), message=message, author=author.username)
        return CreateMessage(message=message_instance)


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('username', 'chats')


class Query(graphene.ObjectType):
    messages_by_chat = graphene.List(MessageType, chat=graphene.String())
    messages_by_id = graphene.Field(MessageType, id=graphene.String())
    chats_by_id = graphene.Field(ChatType, id=graphene.String())
    chats = graphene.List(ChatType)

    def resolve_messages_by_chat(root, info, chat):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged')
        return MessageModel.objects.filter(chat=chat, chat__participants=info.context.user)

    def resolve_messages_by_id(root, info, id):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged')
        return MessageModel.objects.get(pk=id, chat__participants=info.context.user)

    def resolve_chats_by_id(root, info, id):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged')
        return ChatModel.objects.filter(participants=info.context.user).get(pk=id)

    def resolve_chats(root, info, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError('You must be logged')
        # Querying a list
        return ChatModel.objects.filter(participants=info.context.user)


class Mutation(graphene.ObjectType):
    create_message = CreateMessage.Field()
    create_chat = CreateChat.Field()


class OnNewChatMessage(channels_graphql_ws.Subscription):
    """Subscription triggers on a new chat message."""

    author = graphene.String()
    chat = graphene.String()
    message = graphene.String()

    class Arguments:
        """Subscription arguments."""

        chat = graphene.String()

    def subscribe(self, info, chat=None):
        """Client subscription handler."""
        del info
        # Specify the subscription group client subscribes to.
        return [chat] if chat is not None else None

    def publish(self, info, chat=None):
        """Called to prepare the subscription notification message."""

        # The `self` contains payload delivered from the `broadcast()`.
        new_msg_chat = self["chat"]
        new_msg_message = self["message"]
        new_msg_author = self["author"]

        # Method is called only for events on which client explicitly
        # subscribed, by returning proper subscription groups from the
        # `subscribe` method. So he either subscribed for all events or
        # to particular chatroom.
        assert chat is None or chat == new_msg_chat

        # # Avoid self-notifications.
        # if (
        #     info.context.user.is_authenticated
        #     and new_msg_author == info.context.user.username
        # ):
        #     return OnNewChatMessage.SKIP

        return OnNewChatMessage(
            chat=chat, message=new_msg_message, author=new_msg_author
        )

    @classmethod
    def new_chat_message(cls, chat, message, author):
        """Auxiliary function to send subscription notifications.
        It is generally a good idea to encapsulate broadcast invocation
        inside auxiliary class methods inside the subscription class.
        That allows to consider a structure of the `payload` as an
        implementation details.
        """
        cls.broadcast(
            group=chat,
            payload={"chat": chat, "message": message, "author": author},
        )


class Subscription(graphene.ObjectType):
    """GraphQL subscriptions."""

    on_new_chat_message = OnNewChatMessage.Field()
