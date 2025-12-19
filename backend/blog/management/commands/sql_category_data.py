from django.core.management.base import BaseCommand
from blog.models import Category
from typing import Any

class Command(BaseCommand):
    help="seed the data with sample category data"

    def handle(self, *args, **options):
        Category.objects.all().delete()
        
        category =['sports','tecnology','science','art','food']

        for category_name in category:
            Category.objects.create(name= category_name)

        self.stdout.write(self.style.SUCCESS("completed inserting data!"))        
