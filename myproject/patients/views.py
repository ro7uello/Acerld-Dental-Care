from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from datetime import datetime
from .forms import UserRegistrationForm, AppointmentForm
from .models import Appointment, Patient, Profile, PromotionalOffer

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.city_address = form.cleaned_data.get('city_address')
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def redirect_to_dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    elif request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')

@login_required
def admin_dashboard(request):
    total_appointments = Appointment.objects.count()
    registered_patients = Patient.objects.count()
    active_dentists = 15  # Assuming you have a way to count active dentists
    messages = 45  # Assuming you have a way to count messages

    appointments = Appointment.objects.all()

    context = {
        'total_appointments': total_appointments,
        'registered_patients': registered_patients,
        'active_dentists': active_dentists,
        'messages': messages,
        'appointments': appointments,
    }
    return render(request, 'admin_dashboard.html', context)

def landing_page(request):
    promotional_offers = PromotionalOffer.objects.all()
    return render(request, 'landing_page.html', {'promotional_offers': promotional_offers})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(data=request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.user = request.user
                # Convert time_slot string to time object
                hour, minute = map(int, form.cleaned_data['time_slot'].split(':'))
                appointment.time = datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
                appointment.save()
                messages.success(request, 'Appointment booked successfully!')
                return redirect('user_dashboard')
            except Exception as e:
                messages.error(request, f'Error saving appointment: {str(e)}')
    else:
        form = AppointmentForm()
    
    return render(request, 'book_appointment.html', {'form': form})

@login_required
def user_dashboard(request):
    # Get all appointments for the current user
    appointments = Appointment.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'user_dashboard.html', {'appointments': appointments})

@login_required
def get_available_time_slots(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        doctor = request.GET.get('doctor')
        
        if date and doctor:
            form = AppointmentForm()
            time_slots = form.get_available_time_slots(date, doctor)
            return JsonResponse({'time_slots': time_slots})
    
    return JsonResponse({'time_slots': []})