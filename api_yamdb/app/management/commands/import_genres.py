import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Genre.objects.exists():
            print('Файл genre.csv уже загружен.')
        else:
            with open(
                os.path.join(
                    settings.BASE_DIR, 'static/data/genre.csv'
                ), newline=''
            ) as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                for row in reader:
                    Genre.objects.create(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )
        print(Genre.objects.all()[:3])
