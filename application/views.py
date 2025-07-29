from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from .forms import SignupForm, LoginForm, RecipeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserSettingsForm
from .models import Recipe, RecipeTag, Tag
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
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
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def about(request):
    return render(request, 'about.html')

@login_required
def dashboard(request):
    user = request.user
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
    return render(request, 'dashboard.html', {'recipes': recipes, 'user': user})

@login_required
def profile(request, username=None):
    return render(request, 'profile.html', {'username': username})
    #Not proficient enough with HTML and CSS to make it, but definitely needs a button for "logout" that will redirect to the logout_view

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=request.user)
    
    return render(request, 'settings.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def discover(request):
    query = request.GET.get('q', '').strip()
    tag_names = request.GET.getlist('tags')  # pills
    
    recipes = Recipe.objects.filter(is_public=True)

    if query:
        tag_recipe_ids = RecipeTag.objects.filter(
            tag__name__icontains=query
        ).values_list('recipe_id', flat=True)

        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(instructions__icontains=query) |
            Q(id__in=tag_recipe_ids)
        )

    if tag_names:
        for tag in tag_names:
            recipes = recipes.filter(
                recipetag__tag__name__iexact=tag
            )

    return render(request, 'discover.html', {
        'recipes': recipes.distinct(),
        'query': query,
        'selected_tags': tag_names,
        'all_tags': Tag.objects.all(),
    })

@login_required
def post(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
        return redirect('discover')
    else:
        form = RecipeForm()

    return render(request, 'post.html', {'form': form})
