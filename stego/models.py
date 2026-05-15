from django.db import models
from django.contrib.auth.models import User

class StegoOperation(models.Model):
    OPERATION_CHOICES = [
        ('encode', 'Encode'),
        ('decode', 'Decode'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stego_operations')
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    original_filename = models.CharField(max_length=255)
    message_length = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default='success')
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'stego_operation'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['operation_type']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.operation_type} - {self.created_at}"