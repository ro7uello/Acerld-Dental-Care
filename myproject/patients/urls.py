from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import register, user_login, user_dashboard, admin_dashboard, book_appointment, landing_page, redirect_to_dashboard, get_available_time_slots

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('dashboard/', redirect_to_dashboard, name='redirect_to_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('add-profit/', views.add_profit, name='add_profit'),
    path('api/profit-data/', views.get_profit_data, name='get_profit_data'),
    path('api/profit-records/', views.get_profit_records, name='get_profit_records'),
    path('book_appointment/', book_appointment, name='book_appointment'),
    path('get_available_time_slots/', get_available_time_slots, name='get_available_time_slots'),
    path('', landing_page, name='landing_page'),
]