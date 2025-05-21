from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user
from django.contrib import messages
import requests
import json

list_admins = ["admin admin", "admin2 admin2"]

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

    if request.method == 'POST':
        u.nume = request.POST.get('nume')
        u.prenume = request.POST.get('prenume')
        u.email = request.POST.get('email')
        u.parola = request.POST.get('parola')
        u.adresa = request.POST.get('adresa')

        if u.tip_persoana.lower() == 'juridica':
            u.companie = request.POST.get('companie', '')

        u.status_cos = request.POST.get('status_cos') == 'true'

        coords = get_coords_from_address(u.adresa)
        if coords != (None, None):
            u.lat, u.lon = coords

        u.save()

        messages.success(request, "Modificările au fost salvate cu succes!")
        return redirect('/usersapp/dashboard')

    # === Adăugăm locațiile tuturor userilor doar dacă e admin admin ===

    full_name_user = u.nume.lower() + " " + u.prenume.lower()
    user_has_map_access = full_name_user in list_admins
    user_not_has_map_access = full_name_user not in list_admins
    context = {"user": u, "user_has_map_access": user_has_map_access, "user_not_has_map_access": user_not_has_map_access}
    full_name = u.nume.lower() + " " + u.prenume.lower()

    if full_name in list_admins:
        all_users = user.objects.filter(lat__isnull=False, lon__isnull=False)
        user_locations = []
        for usr in all_users:
            full_name_usr = usr.nume.lower() + " " + usr.prenume.lower()
            if full_name_usr not in list_admins:
                try:
                    lat = float(usr.lat)
                    lon = float(usr.lon)
                    user_locations.append({
                        "lat": lat,
                        "lon": lon,
                        "name": f"{usr.nume} {usr.prenume}",
                        "adresa": usr.adresa,
                        "status_cos": usr.status_cos
                    })
                except (ValueError, TypeError):
                    continue
        context["all_user_locations"] = json.dumps(user_locations)

    return render(request, 'dashboard.html', context)


def logout_view(request):
    request.session.flush()
    return redirect('/usersapp/login')



def user_map(request):
    # Obține toți userii care au atât lat, cât și lon definite și numerice
    users = user.objects.filter(lat__isnull=False, lon__isnull=False)

    # Convertim în listă doar userii care au valori numerice valide
    user_locations = []
    for u in users:
        try:
            lat = float(u.lat)
            lon = float(u.lon)
            user_locations.append({
                "lat": lat,
                "lon": lon,
                "name": f"{u.nume} {u.prenume}",
                "adresa": u.adresa
            })
        except (ValueError, TypeError):
            continue  # ignoră userii cu coordonate invalide

    context = {
        "user_locations": json.dumps(user_locations)
    }

    return render(request, "user_map.html", context)
