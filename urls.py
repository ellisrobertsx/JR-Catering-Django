from django.urls import path
from .catering import views
from catering.views import register
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render

urlpatterns = [
    path('', views.index, name='index'),
    path('food_menu/', views.food_menu, name='food_menu'),
    path('drinks_menu/', views.drinks_menu, name='drinks_menu'),
    path('contact/', views.contact, name='contact'),
    path('book/', views.book, name='book'),
    path('create_booking/', views.create_booking, name='create_booking'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('confirmation/<int:booking_id>/', views.confirmation, name='confirmation'),
    path('about/', views.about, name='about'),
    path('register/', register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin/add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('admin/delete_food_item/<int:item_id>/', views.delete_food_item, name='delete_food_item'),
    path('admin/delete_drink_item/<int:item_id>/', views.delete_drink_item, name='delete_drink_item'),
    path('admin/delete_booking/<int:booking_id>/', views.admin_delete_booking, name='admin_delete_booking'),
    path('admin/mark_message_read/<int:message_id>/', views.mark_message_read, name='mark_message_read'),
    path('admin/delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('manifest.json', views.serve_manifest, name='serve_manifest'),
    path('favicon.ico', views.serve_favicon, name='serve_favicon'),
]

def logout_view(request):
    logout(request)
    return redirect('index')  

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index') 
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')