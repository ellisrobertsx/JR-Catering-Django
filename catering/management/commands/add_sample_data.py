from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from catering.models import Booking, FoodItem, DrinkItem, Contact

class Command(BaseCommand):
    help = 'Adds sample data for testing'

    def handle(self, *args, **options):
        # Create sample food items
        food_items = [
            {'name': 'Grilled Salmon', 'category': 'Main Course', 'price': 24.99, 'description': 'Fresh Atlantic salmon with herbs'},
            {'name': 'Beef Tenderloin', 'category': 'Main Course', 'price': 29.99, 'description': 'Premium cut with red wine sauce'},
            {'name': 'Caesar Salad', 'category': 'Appetizer', 'price': 12.99, 'description': 'Classic Caesar with parmesan'},
            {'name': 'Chocolate Cake', 'category': 'Dessert', 'price': 8.99, 'description': 'Rich chocolate layer cake'},
        ]
        
        for item_data in food_items:
            FoodItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
        
        # Create sample drink items
        drink_items = [
            {'name': 'House Red Wine', 'category': 'Wine', 'price': 12.99, 'description': 'Premium red wine selection'},
            {'name': 'Craft Beer', 'category': 'Beer', 'price': 6.99, 'description': 'Local craft brewery selection'},
            {'name': 'Fresh Juice', 'category': 'Non-Alcoholic', 'price': 4.99, 'description': 'Freshly squeezed orange juice'},
        ]
        
        for item_data in drink_items:
            DrinkItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
        
        # Create sample bookings
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
        # Sample bookings for different dates
        booking_dates = [
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=3),
            date.today() + timedelta(days=7),
        ]
        
        sample_bookings = [
            {'name': 'John Smith', 'email': 'john@example.com', 'phone': '555-0101', 'guests': 4, 'special_requests': 'Window seat preferred'},
            {'name': 'Sarah Johnson', 'email': 'sarah@example.com', 'phone': '555-0102', 'guests': 2, 'special_requests': 'Vegetarian options needed'},
            {'name': 'Mike Wilson', 'email': 'mike@example.com', 'phone': '555-0103', 'guests': 6, 'special_requests': 'Birthday celebration'},
        ]
        
        for i, booking_data in enumerate(sample_bookings):
            booking_data.update({
                'user': user,
                'date': booking_dates[i % len(booking_dates)],
                'time': '19:00',
                'status': 'pending' if i == 0 else 'confirmed' if i == 1 else 'pending',
            })
            Booking.objects.get_or_create(
                name=booking_data['name'],
                date=booking_data['date'],
                time=booking_data['time'],
                defaults=booking_data
            )
        
        # Create sample contact messages
        contact_messages = [
            {'name': 'Alice Brown', 'email': 'alice@example.com', 'message': 'Do you cater for corporate events?'},
            {'name': 'Bob Davis', 'email': 'bob@example.com', 'message': 'What are your vegetarian options?', 'is_read': True},
        ]
        
        for msg_data in contact_messages:
            Contact.objects.get_or_create(
                name=msg_data['name'],
                email=msg_data['email'],
                defaults=msg_data
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully added sample data!')
        ) 