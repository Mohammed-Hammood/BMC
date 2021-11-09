from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.dispatch import Signal
from django.db.models.signals import (
    post_save, pre_save, post_delete, pre_delete,
    post_init, pre_init, post_migrate, pre_migrate, m2m_changed
)

from account.models import ProfileModel
from book.models import BookModel, BookCommentModel

level_choices = [
    ('info', 'Info',),
    ('warning', 'Warning',),
    ('success', 'Success',),
    ('permission', 'Permission',),
]


def add_notification_to_followers(actor, type, notification_pk, target=None):
    notification = get_object_or_404(NotificationModel, pk=notification_pk)
    if type == "comment":
        user_notification = get_object_or_404(UserNotificationModel, user=actor)
        if user_notification.user != actor:
            user_notification.unread_notifications.add(notification)
        else:
            pass
    elif type == "lecture":
        profile = get_object_or_404(ProfileModel, user=actor)
        for follower in profile.follow.all():
            qs = UserNotificationModel.objects.get_or_create(
                user=follower
            )
            follower_notification = get_object_or_404(UserNotificationModel, user=follower)
            follower_notification.unread_notifications.add(notification)
    elif type == "follow":
        qs = UserNotificationModel.objects.get_or_create(
            user=target
        )
        uploader = get_object_or_404(UserNotificationModel, user=target)
        uploader.unread_notifications.add(notification)
    else:
        model = get_object_or_404(ProfileModel, user=actor)
        for user in model.follow.all():
            user_notification = get_object_or_404(UserNotificationModel, user=user)
            user_notification.unread_notifications.add(notification)


class NotificationModel(models.Model):
    level = models.CharField(choices=level_choices, blank=True, max_length=100, default=level_choices[0])
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    message = models.TextField(max_length=50)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True, null=True)
    actor_object_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    actor_object_id = models.CharField(max_length=255, null=True)
    actor_content_object = GenericForeignKey("actor_object_content_type", "actor_object_id")
    target_object_content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, related_name='target')
    target_object_id = models.CharField(max_length=255, null=True)
    target_content_object = GenericForeignKey('target_object_content_type', 'target_object_id')
    unread = models.NullBooleanField(default=True, blank=True)
    emailed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self, **kwargs):
        return reverse("notifications_app:home")

    def read_notification(self):
        self.read = True
        self.save()


class UserNotificationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unread_notifications = models.ManyToManyField(NotificationModel, blank=True, related_name='unread_notifications')
    read_notifications = models.ManyToManyField(NotificationModel, blank=True, related_name='read_notifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


def create_notification_by_comment(sender, instance, *args, **kwargs):
    if instance is not None:
        new_notification = NotificationModel(
            user=instance.user,
            link=instance.book.get_absolute_url(),
            message="commented on your book",
            target_content_object=instance,
            actor_content_object=instance.user,

            description="some description",
            unread=True,
            emailed=False,
        )
        new_notification.save()
        add_notification_to_followers(instance.book.user, "comment", new_notification.id)
    else:
        return None


def create_user_notification_for_new_users(sender, instance, *args, **kwargs):
    if instance:
        qs = UserNotificationModel.objects.filter(user=instance).exists()
        if qs is False:
            notification = UserNotificationModel.objects.create(user=instance)
    else:
        pass


post_save.connect(create_user_notification_for_new_users, sender=User, weak=False)
post_save.connect(create_notification_by_comment, sender=BookCommentModel, weak=False)
