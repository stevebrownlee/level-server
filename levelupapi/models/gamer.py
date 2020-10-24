"""Gamer class module"""
from django.db import models
from django.conf import settings


class Gamer(models.Model):
    """Gamer model class"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
