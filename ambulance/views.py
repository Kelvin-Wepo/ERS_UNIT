from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
import africastalking

def home(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'public/index.html', {'feedbacks': feedbacks})

def volunteer_home(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'volunteers/volunteer_home.html', {'feedbacks': feedbacks})

def services(request):
    emergency_services = EmergencyService.objects.all()
    return render(request, 'public/services.html', {'emergency_services': emergency_services})

def public_register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            profile, created = Profile.objects.get_or_create(user=user)

            phone_number = form.cleaned_data.get('contact_number')
               
            if phone_number:
                profile.contact_number = phone_number
                profile.save()
                # SMS sending logic (you may want to move this to a separate function or task)
                africastalking_username = 'kwepo'
        africastalking_api_key = africastalking.api_key
            
        africastalking.initialize(africastalking_username, africastalking_api_key)
        sms = africastalking.SMS
        message = "Welcome to ERS Emergency Service."
        response = sms.send(message, [phone])
        return redirect('login')
    else:
        msg = 'form is not valid'
    
        form = SignUpForm()
    return render(request, 'logins/register.html', {'form': form, 'msg': msg})

def user_login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_volunteer:
                login(request, user)
                return redirect('volunteer_home')
            elif user is not None and user.is_public:
                login(request, user)
                return redirect('home')
            elif user is not None and user.is_admin:
                login(request, user)
                return redirect('admin')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'logins/login.html', {'form': form, 'msg': msg})

def admin(request):
    return render(request, 'admin.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def profile(request):
    users = User.objects.all()
    current_user = request.user
    return render(request, 'profile/profile.html', {"users": users})

def volunteer_profile(request):
    users = User.objects.all()
    current_user = request.user
    return render(request, 'profile/volunteer_profile.html', {"users": users})

def update_profile(request):
    if request.method == 'POST':
        userprofileform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if userprofileform.is_valid():
            userprofileform.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile/update_profile.html', {'form': form})

def volunteer_update_profile(request):
    if request.method == 'POST':
        userprofileform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if userprofileform.is_valid():
            userprofileform.save()
            return redirect('volunteer_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile/volunteer_update_profile.html', {'form': form})

def volunteers(request):
    opportunities = VolunteerOpportunity.objects.all()
    return render(request, 'volunteers/volunteer_home.html', {'opportunities': opportunities})

def add_emergency_service(request):
    if request.method == 'POST':
        form = EmergencyServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            return redirect('volunteer_home')
    else:
        form = EmergencyServiceForm()
    return render(request, 'volunteers/add_service.html', {'form': form})

def single_service(request, service_id):
    service = get_object_or_404(EmergencyService, id=service_id)
    bookings = Booking.objects.filter(service=service)
    return render(request, 'volunteers/single_service.html', {'service': service, 'bookings': bookings})

def delete_service(request, service_id):
    service = get_object_or_404(EmergencyService, id=service_id)
    service.delete()
    return redirect('volunteer_home')

def update_service(request, service_id):
    service = get_object_or_404(EmergencyService, id=service_id)
    if request.method == 'POST':
        form = EmergencyServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('single_service', service_id)
    else:
        form = EmergencyServiceForm(instance=service)
    return render(request, 'volunteers/update_service.html', {'form': form})

def user_single_service(request, service_id):
    service = get_object_or_404(EmergencyService, id=service_id)
    form = FeedbackForm()
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.service = service
            feedback.save()
            return redirect('single_service', service_id)
    
    return render(request, 'public/single_service.html', {'service': service, 'form': form})

def book_service(request, service_id):
    service = get_object_or_404(EmergencyService, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            return redirect('single_service', service_id)
    else:
        form = BookingForm()
    return render(request, 'public/book_service.html', {'form': form, 'service': service})

def add_volunteer_opportunity(request):
    if request.method == 'POST':
        form = VolunteerOpportunityForm(request.POST, request.FILES)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.created_by = request.user
            opportunity.save()
            return redirect('volunteer_home')
    else:
        form = VolunteerOpportunityForm()
    return render(request, 'volunteers/add_opportunity.html', {'form': form})

def apply_volunteer(request, opportunity_id):
    opportunity = get_object_or_404(VolunteerOpportunity, id=opportunity_id)
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.opportunity = opportunity
            application.save()
            return redirect('volunteer_home')
    else:
        form = VolunteerApplicationForm()
    return render(request, 'public/apply_volunteer.html', {'form': form, 'opportunity': opportunity})