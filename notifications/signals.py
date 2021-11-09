from django.contrib.auth.models import User
from .models import NotificationModel, UserNotificationModel, add_notification_to_followers


def notification(type, level=None,user=None, message=None, link=None, description=None, actor_content_object=None,
                 target_content_object=None):
    created = NotificationModel.objects.create(
        user=user,
        link=link,
        message=message,
        actor_content_object=actor_content_object,
        target_content_object=target_content_object,
    )
    add_notification_to_followers(actor=user, type=type, notification_pk=created.pk, target=target_content_object)
