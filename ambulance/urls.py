from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('public_register/', views.public_register, name='register'),
    
    path('login/', views.user_login, name='login'),
    
    path('admin/', views.admin, name='admin'),
    
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/', views.profile, name='profile'),
    
    path('volunteer/profile/', views.volunteer_profile, name='volunteer_profile'),
    
    path('update_profile/', views.update_profile, name='update'),
    
    path('volunteer/update_profile/', views.volunteer_update_profile, name='volunteer_update'),
    
    path('volunteer_home/', views.volunteers, name='volunteer_home'),
    
    path('add_emergency_service/', views.add_emergency_service, name='add_service'),
    
    path('service/<int:service_id>/', views.single_service, name='single_service'),
    
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    
    path('services/', views.services, name='services'),
    
    path('user_service/<int:service_id>/', views.user_single_service, name='user_single_service'),

    path('book-service/<int:service_id>/', views.book_service, name='book_service'),  # Correct URL pattern
    path('booking-success/', views.booking_success, name='booking_success'),
    path('add_volunteer_opportunity/', views.add_volunteer_opportunity, name='add_opportunity'),
    
    path('apply_volunteer/<int:opportunity_id>/', views.apply_volunteer, name='apply_volunteer'),
    
    # Keep these paths if you still need them
]