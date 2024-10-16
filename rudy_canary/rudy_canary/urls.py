from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GitHubTokenViewSet, RepositoryViewSet, fetch_github_repos, github_repos_view, github_oauth_callback

router = DefaultRouter()
# router.register(r'github_tokens', GitHubTokenViewSet, basename='githubtoken')
# router.register(r'repositories', RepositoryViewSet, basename='repository')

urlpatterns = [
    path('api/', include(router.urls)),
    path('github/repos', github_repos_view, name='github_repos'),
    path('github/callback/', github_oauth_callback, name='github_oauth_callback'),

    # path('auth/', include('allauth.urls')),  # Use allauth for authentication paths
    # path('accounts/', include('social_django.urls', namespace='social')),  # Separate namespace for social_django
        # Dj-rest-auth URLs
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    # Allauth social login
    path('api/auth/social/', include('allauth.socialaccount.urls')),
]
