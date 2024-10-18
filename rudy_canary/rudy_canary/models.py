from django.db import models
from django.contrib.auth.models import User

class GitHubToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # user = User.objects.get(email="rudysanchez93@gmail.com")  # Adjust the email to your test case
    github_token = models.CharField(max_length=255)
    github_user = models.CharField(max_length=255)

    def __str__(self):
        return self.github_user