from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout
from .forms import SignupForm, LoginForm, RecipeForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserSettingsForm
from .models import Recipe, RecipeTag, Tag, RecipeStatusTag
from django.db.models import Q

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Added so that home redirects to dashboard when signed in
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
    if request.user.is_authenticated:
        return render(request, 'about_loggedin.html')
    return render(request, 'about_loggedout.html')

@login_required
def dashboard(request):
    user = request.user
    recipes = Recipe.objects.filter(is_public=True).order_by('-created_at')[:3]
    return render(request, 'dashboard.html', {'recipes': recipes, 'user': user})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserSettingsForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def discover(request):
    query = request.GET.get('q', '').strip()
    tag_names = request.GET.getlist('tags')  
    
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
        recipeForm = RecipeForm(request.POST)
        imageForm = ImageForm(request.POST, request.FILES)
        if recipeForm.is_valid() and imageForm.is_valid():
            recipe = recipeForm.save(commit=False)
            recipe.author = request.user
            recipe.save()

            image = imageForm.save(commit=False)
            image.recipe = recipe
            image.save()
        return redirect('discover')
    else:
        recipeForm = RecipeForm()
        imageForm = ImageForm()

    return render(request, 'post.html', {'recipeForm': recipeForm, 'imageForm': imageForm})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(
        Recipe.objects.select_related('author')
                      .prefetch_related('images', 'reviews', 'comments', 'recipetag_set__tag'),
        id=recipe_id
    )

    if not recipe.is_public and recipe.author != request.user:
        return redirect('discover')

    saved_tag = RecipeStatusTag.objects.filter(user=request.user, recipe=recipe).first()

    if request.method == 'POST':
        if 'save_recipe' in request.POST and not saved_tag:
            RecipeStatusTag.objects.create(
                user=request.user,
                recipe=recipe,
                status='want_to_make'
            )
            return redirect('recipe_detail', recipe_id=recipe_id)

        elif 'update_status' in request.POST and saved_tag:
            new_status = request.POST.get('status')
            if new_status in ['want_to_make', 'making', 'made']:
                saved_tag.status = new_status
                saved_tag.save()
                return redirect('recipe_detail', recipe_id=recipe_id)

    return render(request, 'recipe.html', {
        'recipe': recipe,
        'saved_tag': saved_tag,  
    })

@login_required
def user_recipes(request):
    selected_status = request.GET.get("status", "")  
    all_statuses = {
        "want_to_make": "Want To Make",
        "making": "Currently Making",
        "made": "Made"
    }
    tags = RecipeStatusTag.objects.filter(user=request.user).select_related('recipe')

    if selected_status in all_statuses:
        tags = tags.filter(status=selected_status)
    return render(request, 'user_recipes.html', {
        'status_tags': tags,
        'all_statuses': all_statuses,
        'selected_status': selected_status,
    })
