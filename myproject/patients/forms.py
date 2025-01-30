from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Appointment
from datetime import datetime, time, timedelta
from django.core.exceptions import ValidationError
import re
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required')
    city_address = forms.CharField(max_length=100, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'city_address', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('Password must contain at least one special character.')
        if 'password' in password.lower():
            raise ValidationError('Password is too common.')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match") 
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
        
class AppointmentForm(forms.ModelForm):
    DOCTOR_CHOICES = [
        ('Dr. Smith', 'Dr. Smith'),
        ('Dr. Johnson', 'Dr. Johnson'),
        ('Dr. Williams', 'Dr. Williams'),
    ]
    
    doctor = forms.ChoiceField(choices=DOCTOR_CHOICES)
    # Remove the default time field as we'll use our custom time_slot field
    time_slot = forms.ChoiceField(choices=[], label="Available Time Slots")
    
    class Meta:
        model = Appointment
        fields = ['date', 'doctor', 'service', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'service': forms.Select(choices=[
                ('Consultation', 'Consultation'),
                ('Check-Up', 'Check-Up'),
                ('Follow-Up', 'Follow-Up')
            ]),
            'notes': forms.Textarea(attrs={'placeholder': 'Any specific details...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get the date from POST data if it exists
        if 'data' in kwargs and kwargs['data'].get('date'):
            selected_date = kwargs['data'].get('date')
            selected_doctor = kwargs['data'].get('doctor')
            self.fields['time_slot'].choices = self.get_available_time_slots(selected_date, selected_doctor)
        else:
            self.fields['time_slot'].choices = []

    def get_available_time_slots(self, selected_date, selected_doctor):
        # Generate all possible time slots
        time_slots = []
        start_time = time(9, 0)  # 9 AM
        end_time = time(17, 0)   # 5 PM
        
        # Get all booked appointments for the selected date and doctor
        booked_times = Appointment.objects.filter(
            date=selected_date,
            doctor=selected_doctor
        ).values_list('time', flat=True)

        # Convert booked_times to a list of time objects
        booked_slots = [t for t in booked_times]

        # Generate available time slots
        current_time = start_time
        while current_time <= end_time:
            if current_time not in booked_slots:
                time_str = current_time.strftime('%H:%M')
                time_slots.append((time_str, time_str))
            current_time = (datetime.combine(datetime.min, current_time) + timedelta(hours=1)).time()

        return time_slots

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')
        doctor = cleaned_data.get('doctor')

        if date and time_slot and doctor:
            # Convert time_slot string to time object
            hour, minute = map(int, time_slot.split(':'))
            appointment_time = time(hour, minute)

            # Check if the appointment already exists
            if Appointment.objects.filter(
                date=date,
                time=appointment_time,
                doctor=doctor
            ).exists():
                raise forms.ValidationError('This time slot is already booked.')

        return cleaned_data