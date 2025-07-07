from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import *


def dashboard(request):
    return render(request, 'application/dashboard.html')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['user_name'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.save()
    else:
        form = UserForm()
    return render(request, "application/signup.html", {"form": form})

def login(request):
    return HttpResponse('Login')

def profile(request):
    return HttpResponse('Profile')