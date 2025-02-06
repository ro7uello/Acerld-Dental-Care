from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from . import views
from .views import register, user_login, user_dashboard, admin_dashboard, book_appointment, landing_page, get_available_time_slots

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add-review/', views.add_review, name='add_review'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-profit/', views.add_profit, name='add_profit'),
    path('api/profit-data/', views.get_profit_data, name='get_profit_data'),
    path('api/profit-records/', views.get_profit_records, name='get_profit_records'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('get_available_time_slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('', views.landing_page, name='landing_page'),
]