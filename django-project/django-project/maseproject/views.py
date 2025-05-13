from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

def despre(request):
    return render(request, 'despre.html')

def contact(request):
    return render(request, 'contact.html')