import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Category.objects.exists():
            print('Файл category.csv уже загружен.')
        else:
            with open(
                os.path.join(
                    settings.BASE_DIR, 'static/data/category.csv'
                ), newline=''
            ) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader, None)
                for row in reader:
                    Category.objects.create(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )
        print(Category.objects.all())
