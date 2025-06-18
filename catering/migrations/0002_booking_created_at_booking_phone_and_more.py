
from django.db import migrations, models
import django.utils.timezone
from django.contrib.auth.models import User

def set_default_user(apps, schema_editor):
    Booking = apps.get_model('catering', 'Booking')
    User = apps.get_model('auth', 'User')
    # Get or create a default user (e.g., superuser)
    default_user, _ = User.objects.get_or_create(username='default_user', defaults={'email': 'default@example.com'})
    # Assign default user to bookings with NULL user
    Booking.objects.filter(user__isnull=True).update(user=default_user)

class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0001_initial'),  # Adjust if different
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='Booking',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='Booking',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='Booking',
            name='special_requests',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='Booking',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='Booking',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='Booking',
            name='time',
            field=models.CharField(max_length=5),
        ),
        migrations.RunPython(set_default_user),  # Handle NULL user
        migrations.AlterField(
            model_name='Booking',
            name='user',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, related_name='bookings', to='auth.user'),
        ),
    ]