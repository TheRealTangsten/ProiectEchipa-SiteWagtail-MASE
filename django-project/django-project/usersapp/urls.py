from django.urls import path
from . import views

# URL Congiguration
urlpatterns = [
    path('hello/', views.say_hello),
    path('register/', views.register),
    path('login', views.login)
]