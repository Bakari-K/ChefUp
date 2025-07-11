from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('user_dashboard') 
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def about(request):
    return render(request, 'about.html')

@login_required
def dashboard(request):
    recipes = [
        {
            'emote': '🍣',
            'title': 'Spicy Tuna Sushi Rolls',
            'rating': 4
        },
        {
            'emote': '🥗',
            'title': 'Mediterranean Quinoa Bowl',
            'rating': 4
        },
        {
            'emote': '🍲',
            'title': 'Slow Cooker Chili',
            'rating': 5
        }
    ]
    # Once database setup we should replace the recipes with a database query
    return render(request, 'dashboard.html', {'recipes': recipes})
