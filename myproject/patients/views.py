from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.utils import timezone
from django.utils.timezone import make_aware
from django.urls import reverse
from django.http import JsonResponse
from datetime import datetime, timedelta
from .forms import RegistrationForm, AppointmentForm, ProfileCreationForm, UserLoginForm
from .models import Appointment, Patient, PromotionalOffer, Profit, Review
from django.contrib.auth.models import User
import json

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            phone_number = form.cleaned_data['phone_number']
            city_address = form.cleaned_data['city_address']

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email address already exists.')
                return render(request, 'register.html', {'form': form})

            # Create user and patient
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            Patient.objects.create(user=user, phone_number=phone_number, city_address=city_address, email=email)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('redirect_to_dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()
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
    total_reviews = Review.objects.count()

    appointments = Appointment.objects.all().order_by('date', 'time')

    today = timezone.localtime(timezone.now()).date()
    todays_reviews = Review.objects.filter(created_at__date=today)

    context = {
        'total_appointments': total_appointments,
        'registered_patients': registered_patients,
        'active_dentists': active_dentists,
        'total_reviews': total_reviews,
        'todays_reviews': todays_reviews,
        'appointments': appointments,
    }
    return render(request, 'admin_dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')

def landing_page(request):
    promotional_offers = PromotionalOffer.objects.all()
    return render(request, 'landing_page.html', {
        'promotional_offers': promotional_offers
    })

@login_required
def book_appointment(request):
    hours = ["09", "10", "11", "12", "13", "14", "15", "16", "17"]
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time_str = request.POST.get('time_slot')
        service = request.POST.get('service')
        other_type = request.POST.get('otherType')
        material_type = request.POST.get('materialType')
        notes = request.POST.get('notes')

        # Convert time string to time object
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        # Create service description
        service_description = service
        if other_type:
            service_description += f" - {other_type}"
        if material_type:
            service_description += f" ({material_type})"

        # Check if time slot is available
        if Appointment.objects.filter(date=date, time=time_obj).exists():
            messages.error(request, 'This time slot is already taken. Please choose another time.')
            return render(request, 'book_appointment.html', {'hours': hours})

        # Create and save appointment
        appointment = Appointment(
            user=request.user,
            date=date,
            time=time_obj,
            service=service_description,
            notes=notes
        )
        appointment.save()
        
        messages.success(request, 'Appointment booked successfully!')
        return redirect('user_dashboard')
    
    return render(request, 'book_appointment.html', {'hours': hours})

def user_dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = Patient.objects.create(
            user=request.user,
            phone_number='',
            city_address=''
        )
    
    appointments = Appointment.objects.filter(user=request.user)
    context = {
        'appointments': appointments,
        'patient': patient  # Make sure this is passed to the template
    }
    return render(request, 'user_dashboard.html', context)

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

@csrf_exempt
def add_profit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        profit_date = data.get('profitDate')
        profit_amount = data.get('profitAmount')

        # Convert naive datetime to aware datetime in the local timezone, then convert to UTC
        profit_date = timezone.make_aware(datetime.strptime(profit_date, '%Y-%m-%d'), timezone.get_current_timezone())

        # Save to database
        Profit.objects.create(amount=profit_amount, date_logged=profit_date)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

def get_profit_data(request):
    today = timezone.localtime(timezone.now()).date()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)
    
    daily_profits = Profit.objects.filter(date_logged__date=today)
    monthly_profits = Profit.objects.filter(date_logged__date__gte=start_of_month)
    yearly_profits = Profit.objects.filter(date_logged__date__gte=start_of_year)

    daily_data = sum(profit.amount for profit in daily_profits)
    monthly_data = sum(profit.amount for profit in monthly_profits)
    yearly_data = sum(profit.amount for profit in yearly_profits)

    data = {
        'daily': float(daily_data),
        'monthly': float(monthly_data),
        'yearly': float(yearly_data),
    }
    return JsonResponse(data)

def get_profit_records(request):
    profits = Profit.objects.all().order_by('-date_logged')
    records = [
        {
            'id': profit.id,
            'date': timezone.localtime(profit.date_logged).strftime('%Y-%m-%d'),
            'amount': float(profit.amount),  # Ensure amount is a float
        }
        for profit in profits
    ]
    return JsonResponse({'records': records})

@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        review_text = data.get('review_text')
        user = request.user

        print('Received review:', review_text)  # Debugging line

        # Save to database
        Review.objects.create(user=user, review_text=review_text)
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)