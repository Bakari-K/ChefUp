from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'application/dashboard.html')

def signup(request):
    pass