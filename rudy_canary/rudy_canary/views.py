from rest_framework import viewsets
from .models import GitHubToken, Repository
from .serializers import GitHubTokenSerializer, RepositorySerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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

        webhook_url = 'https://your-backend-app.com/github/webhook/'  # URL for receiving webhooks
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
