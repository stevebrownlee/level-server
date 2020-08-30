from django.db import models
from . import Event, Gamer


class EventGamers(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE, related_name="registrations")
