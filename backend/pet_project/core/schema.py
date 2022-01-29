import graphene
from graphene import String
from graphene_django import DjangoObjectType

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
        message_instance = MessageModel(
            message=message_data.message,
            author=info.context.user,
            chat=ChatModel.objects.get(id=message_data.chat)
        )
        message_instance.save()
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
        return MessageModel.objects.filter(chat=chat, chat__participants=info.context.user)

    def resolve_messages_by_id(root, info, id):
        return MessageModel.objects.get(pk=id, chat__participants=info.context.user)

    def resolve_chats_by_id(root, info, id):
        return ChatModel.objects.filter(participants=info.context.user).get(pk=id)

    def resolve_chats(root, info, **kwargs):
        # Querying a list
        return ChatModel.objects.filter(participants=info.context.user)


class Mutation(graphene.ObjectType):
    create_message = CreateMessage.Field()
    create_chat = CreateChat.Field()
