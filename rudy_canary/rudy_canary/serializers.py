from rest_framework import serializers
from .models import GitHubToken, Repository

class GitHubTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubToken
        fields = '__all__'

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'
