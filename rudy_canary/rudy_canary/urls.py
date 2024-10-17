from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import github_repos_view, github_oauth_callback
from django.contrib.auth import views as auth_views


router = DefaultRouter()


urlpatterns = [
    # Add this for the login URL
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    # GitHub Repositories
    path('github/repos', github_repos_view, name='github_repos'),

    # OAuth callback
    path('github/callback/', github_oauth_callback, name='github_oauth_callback'),

    # Authentication paths
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/social/', include('allauth.socialaccount.urls')),
]
