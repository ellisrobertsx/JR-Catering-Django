from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import FoodItem, Booking
from django.utils import timezone

class CateringTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        FoodItem.objects.create(name='Test Food', description='Test', price=9.99, category='Starters')
        Booking.objects.create(
            user=self.user,
            name='Test Booking',
            email='test@example.com',
            phone='1234567890',
            date=timezone.now().date(),
            time='12:00',
            guests=4
        )

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_food_menu(self):
        response = self.client.get(reverse('food_menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Food')

    def test_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass',
            'confirm-password': 'newpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)