from django.db import models

from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(default='', max_length=20,
                                    verbose_name='Номер телефона')