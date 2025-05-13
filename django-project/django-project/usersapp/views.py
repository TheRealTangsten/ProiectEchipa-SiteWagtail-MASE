from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user
from django.contrib import messages
import requests


def get_coords_from_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'FiiVerdeApp/1.0'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print("Eroare geocodare:", e)

    return None, None


def say_hello(request):
    ls = user.objects.get(id=id)
    return HttpResponse("Hello, World!")

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def register_view(request):
    if request.method == 'POST':
        nume = request.POST.get('last_name')
        prenume = request.POST.get('first_name')
        email = request.POST.get('email')
        parola = request.POST.get('password')
        adresa = request.POST.get('address')
        companie = request.POST.get('company_name', '').strip()

        tip_persoana = 'Juridică' if companie else 'Fizică'
        status_cos = False  # implicit: containerul e gol

        # Creează și salvează obiectul user
        user.objects.create(
            nume=nume,
            prenume=prenume,
            email=email,
            parola=parola,
            adresa=adresa,
            companie=companie,
            tip_persoana=tip_persoana,
            status_cos=status_cos
        )

        return redirect('/usersapp/login')  # sau altă pagină de confirmare

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        parola = request.POST.get('password')

        try:
            u = user.objects.get(email=email, parola=parola)
            request.session['user_id'] = u.id
            return redirect('/usersapp/dashboard')  # redirecționează după autentificare
        except user.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email sau parolă incorecte'})

    return render(request, 'login.html')


def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/usersapp/login')

    u = user.objects.get(id=user_id)
    return render(request, 'dashboard.html', {'user': u})


def logout_view(request):
    request.session.flush()
    return redirect('/usersapp/login')


def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/usersapp/login')

    u = user.objects.get(id=user_id)

    if request.method == 'POST':
        u.nume = request.POST.get('nume')
        u.prenume = request.POST.get('prenume')
        u.email = request.POST.get('email')
        u.parola = request.POST.get('parola')
        u.adresa = request.POST.get('adresa')

        if u.tip_persoana == 'juridica':
            u.companie = request.POST.get('companie', '')

        u.status_cos = request.POST.get('status_cos') == 'true'
        
        coords = get_coords_from_address(u.adresa)
        if coords != (None, None):
            u.lat, u.lon = coords
            
        u.save()

        # ✅ Aici pui mesajul:
        messages.success(request, "Modificările au fost salvate cu succes!")

        return redirect('/usersapp/dashboard')

    return render(request, 'dashboard.html', {'user': u})


