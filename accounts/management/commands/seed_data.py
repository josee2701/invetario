from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed initial groups (Admin, Visit)"

    def handle(self, *args, **options):
        client_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Created group 'Admin'"))
        else:
            self.stdout.write("⚠️ Group 'Admin' already exists")

        driver_group, created = Group.objects.get_or_create(name='Visit')
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Created group 'Visit'"))
        else:
            self.stdout.write("⚠️ Group 'Visit' already exists")
