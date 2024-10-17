from rest_framework import viewsets
from .models import GitHubToken, Repository
from .serializers import GitHubTokenSerializer, RepositorySerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import GitHubToken
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import requests
from django.shortcuts import redirect
from django.contrib.auth import login
import json

class GitHubTokenViewSet(viewsets.ModelViewSet):
    queryset = GitHubToken.objects.all()
    serializer_class = GitHubTokenSerializer

    @action(detail=False, methods=['post'])
    def create_token(self, request):
        # This action should handle storing GitHub OAuth token for the user
        # For example, after the user authorizes the app with GitHub, you get the token here.
        token = request.data.get('token')
        # Assuming that the user is authenticated and you link the token to the current user.
        GitHubToken.objects.create(user=request.user, access_token=token)
        return Response({'status': 'Token stored successfully!'})

class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    @action(detail=False, methods=['post'])
    def subscribe_webhook(self, request):
        repo_name = request.data.get('repo_name')
        github_token = GitHubToken.objects.filter(user=request.user).first().access_token

        webhook_url = 'https://7424-47-155-147-98.ngrok-free.app /webhooks/github/'  # URL for receiving webhooks
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'name': 'web',
            'active': True,
            'events': ['push', 'pull_request'],  # GitHub events to subscribe to
            'config': {
                'url': webhook_url,
                'content_type': 'json'
            }
        }

        api_url = f'https://api.github.com/repos/{request.user.github_username}/{repo_name}/hooks'
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 201:
            # Store repository and mark it as webhook_subscribed
            repo, created = Repository.objects.get_or_create(user=request.user, name=repo_name)
            repo.webhook_subscribed = True
            repo.save()
            return Response({'message': 'Webhook subscribed successfully!'})
        else:
            return Response({'message': 'Failed to subscribe to webhook', 'details': response.json()})



def github_oauth_callback(request):
    # Process the GitHub OAuth response and obtain the token
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    # Exchange the code for an access token with GitHub
    response = requests.post('https://github.com/login/oauth/access_token', data={
        'client_id': settings.SOCIAL_AUTH_GITHUB_KEY,
        'client_secret': settings.SOCIAL_AUTH_GITHUB_KEY,
        'code': code,
    }, headers={'Accept': 'application/json'})

    token_response = response.json()
    access_token = token_response.get('access_token')

    if access_token:
        # Save the token in the GitHubToken model
        github_token, created = GitHubToken.objects.get_or_create(user=request.user)
        github_token.github_token = access_token
        github_token.save()

        # Log the user in (if needed)
        login(request, request.user)

        # Redirect to the repos view
        return redirect('github_repos')
    else:
        return JsonResponse({'error': 'Failed to obtain access token'}, status=400)

# @login_required
def github_repos_view(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the user's GitHub token
    try:
        github_token = GitHubToken.objects.get(user=request.user).github_token
    except GitHubToken.DoesNotExist:
        return JsonResponse({'error': 'GitHub token not found'}, status=400)

    # Prepare the API request to GitHub
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # GitHub API endpoint to get the list of repositories
    api_url = "https://api.github.com/user/repos"
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repos = response.json()  # GitHub returns a list of repositories in JSON format
        return JsonResponse(repos, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch repositories', 'details': response.json()}, status=response.status_code)