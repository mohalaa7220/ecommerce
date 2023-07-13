from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('guest', 'guest'),
    )

    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='guest')
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    otp = models.CharField(max_length=4, null=True, blank=True)
    date_joined = models.DateTimeField(
        default=timezone.now, null=True, blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def formatted_date_joined(self):
        return self.date_joined.strftime("%Y-%m-%d %H:%M:%S")

    # def save(self, *args, **kwargs):
    #     self.gender = self.gender.lower()
    #     self.role = self.role.lower()
    #     super(User, self).save(*args, **kwargs)
