from django.contrib import admin
from .models import CustomUser
from graphql_auth.models import UserStatus

admin.site.register(CustomUser)
admin.site.register(UserStatus)