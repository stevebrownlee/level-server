"""Gamer class module"""
from django.db import models
from django.conf import settings


class Gamer(models.Model):
    """Gamer model class"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)

    @property
    def full_name(self):
        """Provides full name for a gamer

        Returns:
            string: Full name of gamer
        """
        return f"{self.user.first_name} {self.user.last_name}"

