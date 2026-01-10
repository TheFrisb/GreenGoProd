from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=DailyItems)
def update_daily_item_slug(sender, instance, created, **kwargs):
    DailyItems.objects.filter(id=instance.pk).update(slug=instance.id)
