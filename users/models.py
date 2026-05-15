from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(blank=True, null=True)
    total_encodes = models.IntegerField(default=0)
    total_decodes = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_profile'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"