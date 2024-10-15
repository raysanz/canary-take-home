from django.contrib import admin
from django.urls import path, include
from rudy_canary.views import github_webhook 
from rest_framework.routers import DefaultRouter
from .views import GitHubTokenViewSet, RepositoryViewSet, fetch_github_repos

router = DefaultRouter()
router.register(r'github_tokens', GitHubTokenViewSet, basename='githubtoken')
router.register(r'repositories', RepositoryViewSet, basename='repository')

urlpatterns = [
    path('api/', include(router.urls)),
    path('github/webhook/', github_webhook, name='github_webhook'),
    path('github/repos/', fetch_github_repos, name='fetch_github_repos'),
    path('auth/', include('allauth.urls')),  # Use allauth for authentication paths
    path('social-auth/', include('social_django.urls', namespace='social')),  # Separate namespace for social_django
]
