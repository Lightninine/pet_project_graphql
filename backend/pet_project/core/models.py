from django.db import models

from users.models import CustomUser


class ChatModel(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chats')


class MessageModel(models.Model):
    chat = models.ForeignKey(
        ChatModel, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(CustomUser, related_name='user_messages', on_delete=models.CASCADE)
    message = models.TextField()
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date_time)
