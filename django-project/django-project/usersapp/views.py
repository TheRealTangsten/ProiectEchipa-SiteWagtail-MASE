from django.shortcuts import render
from django.http import HttpResponse
from .models import user

def say_hello(request):
    ls = user.objects.get(id=id)
    return HttpResponse("Hello, World!")


