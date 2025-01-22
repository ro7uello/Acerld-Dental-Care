from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, user_login, user_dashboard, admin_dashboard, book_appointment, landing_page, redirect_to_dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('dashboard/', redirect_to_dashboard, name='redirect_to_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('book_appointment/', book_appointment, name='book_appointment'),
    path('', landing_page, name='landing_page'),
]