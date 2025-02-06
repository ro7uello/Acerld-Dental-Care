from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Appointment, Patient
from datetime import datetime, time, timedelta
from django.core.exceptions import ValidationError
import re

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(required=True)
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
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Patient.objects.create(user=user, phone_number=self.cleaned_data['phone_number'], city_address=self.cleaned_data['city_address'])
        return user
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone_number', 'city_address']
        
class AppointmentForm(forms.ModelForm):
    time_slot = forms.ChoiceField(choices=[], label="Available Time Slots")
    
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot', 'service', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'service': forms.Select(choices=[
                ('Surgery', 'Surgery'),
                ('Fixed Partial Denture', 'Fixed Partial Denture'),
                ('Crown', 'Crown'),
                ('Removable Partial Denture', 'Removable Partial Denture'),
                ('Complete Denture', 'Complete Denture'),
                ('Others', 'Others')
            ]),
            'notes': forms.Textarea(attrs={'placeholder': 'Any specific details...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize time slots
        self.fields['time_slot'].choices = [
            (f"{hour}:00", f"{hour}:00") for hour in range(9, 18)
        ]

    def get_available_time_slots(self, selected_date):
        # Generate all possible time slots with 1-hour intervals
        time_slots = [
            ("09:00", "09:00"),
            ("10:00", "10:00"),
            ("11:00", "11:00"),
            ("12:00", "12:00"),
            ("13:00", "13:00"),
            ("14:00", "14:00"),
            ("15:00", "15:00"),
            ("16:00", "16:00"),
            ("17:00", "17:00")
        ]
        
        # Filter out the time slots that are already taken
        taken_slots = Appointment.objects.filter(date=selected_date).values_list('time', flat=True)
        available_slots = [slot for slot in time_slots if slot[0] not in taken_slots]
        
        return available_slots