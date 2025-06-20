from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create a superuser for Heroku deployment'

    def handle(self, *args, **options):
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(
                self.style.WARNING('Admin user already exists!')
            )
            return

        # Create the superuser
        user = User.objects.create(
            username='admin',
            email='ellisrob1998@hotmail.co.uk',
            password=make_password('admin123456'),
            is_staff=True,
            is_superuser=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser: {user.username}')
        )
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123456')
        self.stdout.write('Please change the password after first login!') 