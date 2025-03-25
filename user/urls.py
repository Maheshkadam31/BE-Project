from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('portfolio/', views.portfolio_detail, name='portfolio_detail'),
    path('service/', views.service_detail, name='service_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('create/', views.create_booking, name='create_booking'),
    path('profile/', views.profile_view, name='profile'),
    path('jjv/', views.jjv, name='jjv'),
    path('a1k/', views.a1k, name='a1k'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

