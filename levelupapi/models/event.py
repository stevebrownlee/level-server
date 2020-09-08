from django.db import models
from . import Game, Gamer


class Event(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=500)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)

    @property
    def joined(self):
        """joined property, which will be calculated per user

        Returns:
            boolean -- If the user has joined the event or not
        """
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
