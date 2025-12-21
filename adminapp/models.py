from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class rdv(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('REJECTED', 'Refusé'),
        ('CANCELLED', 'Annulé'),
    ]

    client_account = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    client = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    date = models.DateField()
    heure = models.TimeField()
    service = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.client}- {self.service} on {self.date} at {self.heure}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Token expires in 1 hour
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at

    def __str__(self):
        return f"Reset token for {self.user.username} - {'Used' if self.used else 'Active'}"