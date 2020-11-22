"""Game DB Model Module"""
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from ..models import Gamer


class Game(models.Model):
    """Representation of a playable game that a gamer can create"""
    gametype = models.ForeignKey("GameType", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    maker = models.CharField(max_length=55)
    gamer = models.ForeignKey(
        Gamer, on_delete=models.CASCADE, related_name="games")
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()

    @property
    def event_count(self):
        return self.__event_count

    @event_count.setter
    def event_count(self, value):
        self.__event_count = value

    @property
    def user_event_count(self):
        return self.__user_event_count

    @user_event_count.setter
    def user_event_count(self, value):
        self.__user_event_count = value


@receiver(pre_save, sender=Game)
# pylint: disable=unused-argument
def skill_level_validate(instance, **kwargs):
    """Ensure that skill level falls within the acceptable range

    Args:
        instance (Game): Game model instance

    Raises:
        ValidationError: Specified skill level is not acceptable
    """
    if instance.skill_level is None or instance.skill_level < 0 or instance.skill_level > 5:
        raise ValidationError(
            f'Invalid skill_level. Valid values are 1-5. Received {instance.skill_level}',
            params={'skill_level': instance.skill_level},
        )
