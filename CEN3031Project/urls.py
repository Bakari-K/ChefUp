"""
URL configuration for CEN3031Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from application import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('discover/' , views.discover, name='discover'),
    path('logout/', views.logout_view, name='logout'),
    path('post/', views.post, name='post'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('my-recipes/', views.user_recipes, name='user_recipes'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('rate/<int:recipe_id>/', views.recipe_rate, name='rate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
