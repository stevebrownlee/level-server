from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):

    gametype = models.ForeignKey("GameType", on_delete=models.CASCADE)
