from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.utils import timezone
from django.utils.timezone import make_aware
from django.http import JsonResponse
from datetime import datetime, timedelta
from .forms import UserRegistrationForm, AppointmentForm, UserLoginForm
from .models import Appointment, Patient, PromotionalOffer, Profit, Review
import json

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
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

    appointments = Appointment.objects.all()

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