"""
authentication urls
"""

# app_name = "authentication"
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from .forms import EmailValidationOnForgotPassword



urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), 
         name='password_reset'),
    path('', include("django.contrib.auth.urls")),
    path('register/', views.register, name="register"),
    path('<int:pk>/', login_required(views.ProfileView.as_view()), name="profile"),
    path('edit-email/', views.edit_email_view, name="edit_email"),
    path("edit-phone/", views.edit_phone_view, name="edit_phone"),
    path("edit-name/", views.edit_name_view, name="edit_name"),
    path('login_redirect/', views.login_redirect, name="login_redirect")
]
