from django.urls import path
from .views import register, user_login, user_dashboard, admin_dashboard, book_appointment

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('book_appointment/', book_appointment, name='book_appointment'),
]