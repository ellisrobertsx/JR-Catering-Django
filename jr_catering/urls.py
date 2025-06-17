from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
##from .models import Booking, MenuItem, Category

def home(request):
    return render(request, 'index.html')

def food_menu(request):
    return render(request, 'food_menu.html')

def drinks_menu(request):
    return render(request, 'drinks_menu.html')

def book(request):
    return render(request, 'book.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return render(request, 'logout.html')

def admin_panel(request):
    return render(request, 'admin_panel.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='index'),
    path('food_menu/', food_menu, name='food_menu'),
    path('drinks_menu/', drinks_menu, name='drinks_menu'),
    path('book/', book, name='book'),
    path('contact/', contact, name='contact'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin_panel/', admin_panel, name='admin_panel'),
]
