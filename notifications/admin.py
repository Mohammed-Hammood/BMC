from django.contrib import admin
from notifications.models import NotificationModel, UserNotificationModel


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',  'message', 'link','target_content_object', 'actor_content_object', 'timestamp']
    list_display_links = ['id', 'user',  'message', 'link', 'target_content_object', 'actor_content_object', 'timestamp']
    list_filter = ['user',  'message', 'timestamp']
    search_fields = [ 'message', ]
    readonly_fields = ['target_content_object', 'actor_content_object', 'timestamp']

    class Meta:
        model = NotificationModel


class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'timestamp', 'update']
    list_display_links = ['id', 'user', 'timestamp', 'update']
    list_filter = ['user', 'timestamp']
    # search_fields = ['user', ]
    readonly_fields = ['timestamp', 'update']

    class Meta:
        model = UserNotificationModel


admin.site.register(NotificationModel, NotificationAdmin)
admin.site.register(UserNotificationModel, UserNotificationAdmin)
