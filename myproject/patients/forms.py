from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required')
    city_address = forms.CharField(max_length=100, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'city_address', 'email', 'password1', 'password2']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
class AppointmentForm(forms.ModelForm):
    DOCTOR_CHOICES = [
        ('Dr. Smith', 'Dr. Smith'),
        ('Dr. Johnson', 'Dr. Johnson'),
        ('Dr. Williams', 'Dr. Williams'),
    ]
    dentist = forms.ChoiceField(choices=DOCTOR_CHOICES)
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'doctor', 'service', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'service': forms.Select(choices=[
                ('Consultation', 'Consultation'),
                ('Check-Up', 'Check-Up'),
                ('Follow-Up', 'Follow-Up')
            ]),
            'notes': forms.Textarea(attrs={'placeholder': 'Any specific details...'}),
        }