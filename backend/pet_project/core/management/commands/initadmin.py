from django.conf import settings  # pragma: no cover
from django.core.management.base import BaseCommand  # pragma: no cover
from users.models import CustomUser  # pragma: no cover


class Command(BaseCommand):  # pragma: no cover

    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            username = 'admin'
            email = ''
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin = CustomUser.objects.create_superuser(email=email,
                                                        username=username,
                                                        password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print(
                'Admin accounts can only be initialized if no Accounts exist')
