import time  # pragma: no cover
from django.db import connections  # pragma: no cover
from django.db.utils import OperationalError  # pragma: no cover
from django.core.management import BaseCommand  # pragma: no cover


class Command(BaseCommand):  # pragma: no cover
    """Django command to pause execution until db is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waititng 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
