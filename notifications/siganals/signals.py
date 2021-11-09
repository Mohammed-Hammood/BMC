from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from notifications.models import NotificationModel
from notifications import models


def create_notification_by_comment(sender, instance, *args, **kwargs):
    print('function starts to execute......')
    if instance is not None:

        new_notification = NotificationModel(
            user=instance.user,
            link=instance.audio.get_absolute_url(),
            message="commented on",
            target_content_object=instance.audio,
            actor_content_object=instance,
            description="some description",
            unread=True,
            emailed=False,
        )
        new_notification.save()
    else:
        print('this signal contains not instance')
        return None


