from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from catering.views import (
    index, register, book, create_booking, edit_booking, delete_booking, 
    food_menu, drinks_menu, contact, login_view, logout_view, confirmation,
    about, add_menu_item, delete_food_item, delete_drink_item, 
    admin_delete_booking, mark_message_read, delete_message,
    serve_manifest, serve_favicon
)
##from .models import Booking, MenuItem, Category

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('food-menu/', food_menu, name='food_menu'),
    path('drinks-menu/', drinks_menu, name='drinks_menu'),
    path('book/', book, name='book'),
    path('contact/', contact, name='contact'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('create_booking/', create_booking, name='create_booking'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('confirmation/<int:booking_id>/', confirmation, name='confirmation'),
    path('add_menu_item/', add_menu_item, name='add_menu_item'),
    path('delete_food_item/<int:item_id>/', delete_food_item, name='delete_food_item'),
    path('delete_drink_item/<int:item_id>/', delete_drink_item, name='delete_drink_item'),
    path('admin_delete_booking/<int:booking_id>/', admin_delete_booking, name='admin_delete_booking'),
    path('mark_message_read/<int:message_id>/', mark_message_read, name='mark_message_read'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('manifest.json', serve_manifest, name='manifest'),
    path('favicon.ico', serve_favicon, name='favicon'),
]
