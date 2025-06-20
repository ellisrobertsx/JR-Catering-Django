from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create a local admin user for development'

    def handle(self, *args, **options):
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            # Update existing admin user
            user = User.objects.get(username='admin')
            user.password = make_password('admin123456')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated existing admin user: {user.username}')
            )
        else:
            # Create new admin user
            user = User.objects.create(
                username='admin',
                email='admin@example.com',
                password=make_password('admin123456'),
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created new admin user: {user.username}')
            )

        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123456')
        self.stdout.write('Staff permissions: True')
        self.stdout.write('Superuser permissions: True') 