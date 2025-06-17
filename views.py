from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import FoodItem, DrinkItem, Booking, Contact
from django.contrib.auth.models import User
import json
import logging

logger = logging.getLogger(__name__)

def index(request):
    logger.debug(f"Index - User authenticated: {request.user.is_authenticated}")
    response = render(request, 'index.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def food_menu(request):
    logger.debug(f"Food_menu - User authenticated: {request.user.is_authenticated}")
    food_items = FoodItem.objects.all()
    menu_items = {}
    for item in food_items:
        menu_items.setdefault(item.category, []).append(item)
    if not food_items:
        messages.info(request, 'No food items available yet.')
    return render(request, 'food_menu.html', {'menu_items': menu_items})

def drinks_menu(request):
    logger.debug(f"Drinks_menu - User authenticated: {request.user.is_authenticated}")
    drink_items = DrinkItem.objects.all()
    menu_items = {}
    for item in drink_items:
        menu_items.setdefault(item.category, []).append(item)
    if not drink_items:
        messages.info(request, 'No drink items available yet.')
    return render(request, 'drinks_menu.html', {'menu_items': menu_items})

def contact(request):
    logger.debug(f"Contact - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        if not all([name, email, message]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            Contact.objects.create(name=name, email=email, phone=phone, message=message)
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')
    return render(request, 'contact.html')

@login_required
def book(request):
    logger.debug(f"Book - User authenticated: {request.user.is_authenticated}")
    bookings = Booking.objects.filter(user=request.user, date__gte=timezone.now().date()).order_by('date', 'time')
    return render(request, 'book.html', {'bookings': bookings})

@login_required
def create_booking(request):
    logger.debug(f"Create_booking - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            date = data.get('date')
            time = data.get('time')
            guests = data.get('guests')
            special_requests = data.get('special_requests', '')
            if not all([name, email, phone, date, time, guests]):
                return JsonResponse({'error': 'All required fields must be filled'}, status=400)
            new_booking = Booking.objects.create(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                date=date,
                time=time,
                guests=int(guests),
                special_requests=special_requests
            )
            return JsonResponse({
                'success': 'Booking created successfully',
                'booking': {
                    'id': new_booking.id,
                    'name': new_booking.name,
                    'email': new_booking.email,
                    'phone': new_booking.phone,
                    'date': new_booking.date,
                    'time': new_booking.time,
                    'guests': new_booking.guests
                }
            })
        except Exception as e:
            logger.error(f"Error in create_booking: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def edit_booking(request, booking_id):
    logger.debug(f"Edit_booking - User authenticated: {request.user.is_authenticated}")
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking.name = data.get('name', booking.name)
            booking.email = data.get('email', booking.email)
            booking.phone = data.get('phone', booking.phone)
            booking.date = data.get('date', booking.date)
            booking.time = data.get('time', booking.time)
            booking.guests = int(data.get('guests', booking.guests))
            booking.save()
            return JsonResponse({'success': 'Booking updated successfully'})
        except Exception as e:
            logger.error(f"Error in edit_booking: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def delete_booking(request, booking_id):
    logger.debug(f"Delete_booking - User authenticated: {request.user.is_authenticated}")
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        try:
            booking.delete()
            return JsonResponse({'success': 'Booking deleted successfully'})
        except Exception as e:
            logger.error(f"Error in delete_booking: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def confirmation(request, booking_id):
    logger.debug(f"Confirmation - User authenticated: {request.user.is_authenticated}")
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_confirmation.html', {'booking': booking})

def about(request):
    logger.debug(f"About - User authenticated: {request.user.is_authenticated}")
    return render(request, 'about.html')

def register(request):
    logger.debug(f"Register - Method: {request.method}")
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                confirm_password = data.get('confirm-password')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid data format'}, status=400)
        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')

        if not all([username, email, password, confirm_password]):
            error_msg = 'Please fill in all fields.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=400)
            messages.error(request, error_msg)
            return render(request, 'register.html')
        if password != confirm_password:
            error_msg = 'Passwords do not match.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=400)
            messages.error(request, error_msg)
            return render(request, 'register.html')
        if User.objects.filter(username=username).exists():
            error_msg = 'Username already exists.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=400)
            messages.error(request, error_msg)
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            error_msg = 'Email already registered.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=400)
            messages.error(request, error_msg)
            return render(request, 'register.html')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            success_msg = 'Registration successful!'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': success_msg, 'redirect': '{% url 'index' %}'})
            messages.success(request, success_msg)
            return redirect('index')
        except Exception as e:
            logger.error(f"Error in register: {str(e)}")
            error_msg = 'Error processing registration.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=500)
            messages.error(request, error_msg)
            return render(request, 'register.html')
    return render(request, 'register.html')

def login_view(request):
    logger.debug(f"Login - Method: {request.method}")
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Please enter username and password.')
            return render(request, 'login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            next_page = request.GET.get('next', 'index')
            if user.is_staff:
                return redirect('admin_panel')
            return redirect(next_page)
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logger.debug(f"Logout - User authenticated: {request.user.is_authenticated}")
    logout(request)
    messages.success(request, 'Logged out successfully.')
    response = redirect('index')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    logger.debug(f"Admin_panel - User authenticated: {request.user.is_authenticated}")
    date_filter = request.GET.get('date_filter')
    bookings = Booking.objects.filter(date=date_filter).order_by('-date') if date_filter else Booking.objects.order_by('-date')
    return render(request, 'admin_panel.html', {
        'food_items': FoodItem.objects.all(),
        'drink_items': DrinkItem.objects.all(),
        'bookings': bookings,
        'messages': Contact.objects.order_by('-created_at')
    })

@user_passes_test(lambda u: u.is_staff)
def add_menu_item(request):
    logger.debug(f"Add_menu_item - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        menu_type = request.POST.get('menu_type')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category') if menu_type == 'food' else request.POST.get('drink_category')
        if not all([menu_type, name, description, price]):
            messages.error(request, 'All fields required.')
        elif menu_type == 'food' and not category:
            messages.error(request, 'Category required for food items.')
        elif menu_type == 'drink' and not category:
            messages.error(request, 'Category required for drink items.')
        else:
            try:
                price = float(price)
                if menu_type == 'food':
                    FoodItem.objects.create(name=name, description=description, price=price, category=category)
                else:
                    DrinkItem.objects.create(name=name, description=description, price=price, category=category)
                messages.success(request, 'Menu item added!')
                return redirect('admin_panel')
            except Exception as e:
                logger.error(f"Error in add_menu_item: {str(e)}")
                messages.error(request, 'Error adding menu item.')
    return render(request, 'admin_menu.html')

@user_passes_test(lambda u: u.is_staff)
def delete_food_item(request, item_id):
    logger.debug(f"Delete_food_item - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        food_item = get_object_or_404(FoodItem, id=item_id)
        food_item.delete()
        messages.success(request, 'Food item deleted!')
    return redirect('admin_panel')

@user_passes_test(lambda u: u.is_staff)
def delete_drink_item(request, item_id):
    logger.debug(f"Delete_drink_item - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        drink_item = get_object_or_404(DrinkItem, id=item_id)
        drink_item.delete()
        messages.success(request, 'Drink item deleted!')
    return redirect('admin_panel')

@user_passes_test(lambda u: u.is_staff)
def admin_delete_booking(request, booking_id):
    logger.debug(f"Admin_delete_booking - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        messages.success(request, 'Booking deleted!')
    return redirect('admin_panel')

@user_passes_test(lambda u: u.is_staff)
def mark_message_read(request, message_id):
    logger.debug(f"Mark_message_read - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        message = get_object_or_404(Contact, id=message_id)
        message.is_read = True
        message.save()
        messages.success(request, 'Message marked as read!')
    return redirect('admin_panel')

@user_passes_test(lambda u: u.is_staff)
def delete_message(request, message_id):
    logger.debug(f"Delete_message - User authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        message = get_object_or_404(Contact, id=message_id)
        message.delete()
        messages.success(request, 'Message deleted!')
    return redirect('admin_panel')

def serve_manifest(request):
    return HttpResponse(open(os.path.join(BASE_DIR, 'static', 'manifest.json')).read(), content_type='application/json')

def serve_favicon(request):
    return HttpResponse(open(os.path.join(BASE_DIR, 'static', 'favicon.ico'), 'rb').read(), content_type='image/x-icon')