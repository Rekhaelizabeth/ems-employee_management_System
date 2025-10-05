# ems/views.py
from django.shortcuts import render

def home(request):
    return render(request, "home.html")  # landing page

def auth_page(request):
    return render(request, "auth.html")  # register/login page

def profile_page(request):
    return render(request, "profile.html")