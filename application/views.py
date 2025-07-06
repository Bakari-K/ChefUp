from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'application/dashboard.html')

def signup(request):
    return HttpResponse('Sign up')

def login(request):
    return HttpResponse('Login')