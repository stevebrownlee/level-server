from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from ..models import Gamer

class Game(models.Model):

    gametype = models.ForeignKey("GameType", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    maker = models.CharField(max_length=55)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE, related_name="games")
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()

@receiver(pre_save, sender=Game)
def skill_level_validate(instance, **kwargs):
    if instance.skill_level < 0 or instance.skill_level > 5:
        raise ValidationError(
            f'Invalid skill_level. Valid values are 1-5. Received {instance.skill_level}',
            params={'skill_level': instance.skill_level},
        )