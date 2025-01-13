from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, AppointmentForm
from .models import Patient, Appointment

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
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
def user_dashboard(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'appointments': appointments})

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

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.dentist = 'Dr. Smith'  # Assign a dentist or handle dynamically
            appointment.save()
            return redirect('user_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})