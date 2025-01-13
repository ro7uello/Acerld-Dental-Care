from django.contrib import admin
from .models import Patient, Appointment

admin.site.register(Patient)
admin.site.register(Appointment)