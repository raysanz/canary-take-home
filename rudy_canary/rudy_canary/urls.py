"""
URL configuration for rudy_canary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from rudy_canary.views import github_webhook 
from rest_framework.routers import DefaultRouter
from .views import GitHubTokenViewSet, RepositoryViewSet

router = DefaultRouter()
router.register(r'github_tokens', GitHubTokenViewSet, basename='githubtoken')
router.register(r'repositories', RepositoryViewSet, basename='repository')


urlpatterns = [
    path('api/', include(router.urls)),
    path('github/webhook/', github_webhook, name='github_webhook'),
]
