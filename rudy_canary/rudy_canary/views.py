from rest_framework import viewsets
from .models import GitHubToken, Repository
from .serializers import GitHubTokenSerializer, RepositorySerializer

class GitHubTokenViewSet(viewsets.ModelViewSet):
    queryset = GitHubToken.objects.all()
    serializer_class = GitHubTokenSerializer

class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
