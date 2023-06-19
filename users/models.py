from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('guest', 'admin'),
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='guest')
    gender = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=4, null=True, blank=True)
    date_joined = models.DateTimeField(
        default=timezone.now, null=True, blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.gender = self.gender.lower()
        self.role = self.role.lower()
        super(User, self).save(*args, **kwargs)
