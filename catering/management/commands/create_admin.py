from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser account'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@jrcatering.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            return
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created superuser "{username}" with password "{password}"'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                'Please change the password after first login for security!'
            )
        ) 