from django.urls import path

from . import views

app_name = 'application'
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
]