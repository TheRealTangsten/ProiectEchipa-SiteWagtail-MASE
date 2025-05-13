from django.urls import path
from . import views

# URL Congiguration
urlpatterns = [
    path('hello/', views.say_hello),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]