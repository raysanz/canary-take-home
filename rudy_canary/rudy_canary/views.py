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


# GitHub webhook receiving endpoint
@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        # Parse the GitHub webhook event payload
        payload = json.loads(request.body.decode('utf-8'))
        event_type = request.headers.get('X-GitHub-Event', None)

        # Handle different event types
        if event_type == 'push':
            print("Push event received:", payload)
        elif event_type == 'pull_request':
            print("Pull request event received:", payload)

        return JsonResponse({'status': 'Webhook received'})
    return JsonResponse({'error': 'Invalid method'}, status=400)

# Example of adding authentication to a view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @login_required  # Ensure the user is logged in
def fetch_github_repos(request):
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_CLIENT_SECRET
    
    github_user =  'raysanz'
        # Check if the user has a GitHub token
    try:
        github_token = settings.SOCIAL_AUTH_GITHUB_TOKEN
    except GitHubToken.DoesNotExist:
        return JsonResponse({'error': 'GitHub token not found'}, status=400)

    # Prepare the API request to GitHub
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    api_url = "https://api.github.com/user/repos"
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        return JsonResponse(repos, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch repositories', 'details': response.json()}, status=response.status_code)
    # url = f"https://api.github.com/users/{github_user}/repos?client_id={client_id}&client_secret={client_secret}"
    # response = requests.get(url)
    # return JsonResponse(response.json(), safe=False)
    # if not request.user.is_authenticated:
    #     print("User not authenticated:", request.user)
    #     return JsonResponse({'error': 'User not authenticated'}, status=401)

    # # Get the user's GitHub access token from the GitHubToken model
    # try:
    #     github_token = GitHubToken.objects.get(user=request.user).github_token
    #     # GitHubToken.objects.get(user=request.user).github_token
    # except GitHubToken.DoesNotExist:
    #     return JsonResponse({'error': 'GitHub token not found'}, status=400)

    # headers = {
    #     'Authorization': f'token {github_token}',
    #     'Accept': 'application/vnd.github.v3+json'
    # }

    # # GitHub API endpoint to get the list of repositories for the authenticated user
    # api_url = "https://api.github.com/user/repos"
    
    # response = requests.get(api_url, headers=headers)

    # if response.status_code == 200:
    #     repos = response.json()  # GitHub will return a list of repositories in JSON format
    #     return JsonResponse(repos, safe=False)
    # else:
    #     return JsonResponse({'error': 'Failed to fetch repositories', 'details': response.json()}, status=response.status_code)
