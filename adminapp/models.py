from django.db import models

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

    def __str__(self):
        return f"{self.client}- {self.service} on {self.date} at {self.heure}"