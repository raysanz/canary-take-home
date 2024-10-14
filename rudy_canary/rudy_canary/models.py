from django.db import models
from django.contrib.auth.models import User

class GitHubToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_token = models.CharField(max_length=255)
    github_user = models.CharField(max_length=255)

    def __str__(self):
        return self.github_user


class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    webhook_url = models.URLField()
