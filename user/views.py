from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.templatetags.static import static
import json
from django.views.decorators.csrf import csrf_exempt

# Import your models and forms
from .models import Post, Booking, Show, Seat, UserProfile
from .forms import SignUpForm, BookingForm

# Home view with portfolio items
def home(request):
    portfolio_items = [
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-2.jpg'), 'title': 'Product 1', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-product'},
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-3.jpg'), 'title': 'Branding 1', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-branding'},
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-4.jpg'), 'title': 'App 2', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-app'},
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-5.jpg'), 'title': 'Product 2', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-product'},
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-6.jpg'), 'title': 'Branding 2', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-branding'},
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-7.jpg'), 'title': 'App 3', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-app'},
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-8.jpg'), 'title': 'Product 3', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-product'},
        {'image': static('assets/img/masonry-portfolio/masonry-portfolio-9.jpg'), 'title': 'Branding 3', 'description': 'Lorem ipsum, dolor sit', 'filter': 'filter-branding'},
    ]
    return render(request, 'home.html', {'portfolio_items': portfolio_items})

# Portfolio detail view
def portfolio_detail(request):
    return render(request, 'portfolio_detail.html')

# Service detail view
def service_detail(request):
    return render(request, 'service-details.html')

# Sign-up view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login')  # Redirect to homepage after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Profile view
@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(user=request.user)  # Assuming Booking has a foreign key to User
    return render(request, 'profile.html', {'user_profile': user_profile, 'bookings': bookings})

# Create booking view with seat selection
@login_required
def create_booking(request):
    show = Show.objects.first()  # Get the first available show
    if not show:
        return render(request, 'no_show_available.html')

    available_seats = show.total_seats - show.booked_seats

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('selected_seats')
        if selected_seat_ids:
            for seat_id in selected_seat_ids:
                seat = Seat.objects.get(id=seat_id)
                seat.is_booked = True
                seat.save()

            # Create booking entry
            booking = Booking.objects.create(
                user=request.user,
                show=show,
                seats=selected_seat_ids  # Save selected seats
            )

            return redirect('payment')  # Redirect to payment page

    return render(request, 'create_booking.html', {'available_seats': available_seats})


# Booking list view
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

# Booking JSON API (AJAX for seat booking)
@csrf_exempt
def book_seats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_seats = data.get('seats', [])

        # Implement seat booking logic here
        for seat_id in selected_seats:
            seat = Seat.objects.get(id=seat_id)
            seat.is_booked = True
            seat.save()

        return JsonResponse({'success': True, })
    return JsonResponse({'success': False})

# Additional static pages
def jjv(request):
    return render(request, 'jjv.html')

def a1k(request):
    return render(request, 'a1k.html')
