# accounts/signals.py

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
import os
from accounts.models import Event  # Ensure this path is correct

@receiver(pre_save, sender=Event)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Event.objects.get(pk=instance.pk).image
        except Event.DoesNotExist:
            return
        else:
            new_image = instance.image
            if old_image and old_image != new_image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)

@receiver(pre_delete, sender=Event)
def delete_image_on_event_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
