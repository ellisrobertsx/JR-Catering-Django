# init_db.py
from django.core.management.base import BaseCommand
from catering.models import FoodItem, DrinkItem

class Command(BaseCommand):
    help = 'Initialize database with menu items'

    def handle(self, *args, **kwargs):
        # Clear existing data
        FoodItem.objects.all().delete()
        DrinkItem.objects.all().delete()
        # Define drinks
        drinks = [
            {'name': 'House Red Wine', 'description': 'Smooth medium-bodied red wine', 'price': 5.99, 'category': 'Wine'},
            {'name': 'House White Wine', 'description': 'Crisp and refreshing white wine', 'price': 5.99, 'category': 'Wine'},
            {'name': 'Prosecco', 'description': 'Light and bubbly Italian sparkling wine', 'price': 6.99, 'category': 'Wine'},
            {'name': 'Draft Beer', 'description': 'Local craft beer on tap', 'price': 4.99, 'category': 'Beer'},
            {'name': 'Bottled Beer', 'description': 'Selection of premium bottled beers', 'price': 3.99, 'category': 'Beer'},
            {'name': 'Mojito', 'description': 'Rum, lime, mint, and soda water', 'price': 7.99, 'category': 'Cocktails'},
            {'name': 'Margarita', 'description': 'Tequila, triple sec, and lime juice', 'price': 7.99, 'category': 'Cocktails'},
            {'name': 'Gin & Tonic', 'description': 'Premium gin with tonic water and lime', 'price': 6.99, 'category': 'Cocktails'},
        ]
        # Define foods
        foods = [
            {'name': 'Garlic Bread', 'description': 'Fresh baked bread with garlic butter', 'price': 4.99, 'category': 'Starters'},
            {'name': 'Caesar Salad', 'description': 'Crisp romaine lettuce, parmesan, croutons, and Caesar dressing', 'price': 9.99, 'category': 'Starters'},
            {'name': 'Classic Burger', 'description': '6oz beef patty with lettuce, tomato, and our special sauce', 'price': 12.99, 'category': 'Mains'},
            {'name': 'Fish & Chips', 'description': 'Beer-battered cod with hand-cut chips and mushy peas', 'price': 14.99, 'category': 'Mains'},
            {'name': 'Chocolate Brownie', 'description': 'Warm chocolate brownie with vanilla ice cream', 'price': 6.99, 'category': 'Desserts'},
            {'name': 'Sticky Toffee Pudding', 'description': 'Classic dessert with butterscotch sauce', 'price': 6.99, 'category': 'Desserts'},
        ]
        # Populate database
        for drink in drinks:
            DrinkItem.objects.create(**drink)
        for food in foods:
            FoodItem.objects.create(**food)
        self.stdout.write(self.style.SUCCESS('Database initialized successfully'))