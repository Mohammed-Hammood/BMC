import html
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import ListView, View, UpdateView, DeleteView, RedirectView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied
from django.core.exceptions import PermissionDenied, ValidationError
from account.models import ProfileModel
from tools.utils import context, get_authenticated_user_objects, get_session_objects
from notifications.models import NotificationModel, UserNotificationModel
from django.contrib.auth.models import User
nothing_json = HttpResponse(json.dumps("None"), content_type="application/json")
nothing_html = HttpResponse(html.escape("None"), content_type="application/html")


@login_required
def notifications_list(request):
    get_authenticated_user_objects(request)
    notifications = get_object_or_404(UserNotificationModel, user=request.user)
    if notifications.unread_notifications.count() > 0:
        x = notifications.unread_notifications.count()
        for item in notifications.unread_notifications.all():
            notifications.unread_notifications.remove(item)
            notifications.read_notifications.add(item)
    else:
        x = 8
    context['notifications'] = notifications.read_notifications.all()[:x]
    # very important note: slicing to profiles from previous view my force some profile picture to
    # disappear so need to rewrite it.
    context['profiles'] = ProfileModel.objects.all()
    return render(request, 'notifications/list.html', context)


def notifications_loader(request):

    count = request.POST.get("objectsCount")
    load_count = request.POST.get("loadCount", None)
    if load_count is not None and int(load_count) > 0:
        increment = int(load_count)
    else:
        increment = 3
    if int(count) < 1:
        count = 3
    y = int(count)
    x = y + increment
    if request.is_ajax() and request.method == "POST":
        notifications = get_object_or_404(UserNotificationModel, user=request.user)
        if notifications.unread_notifications.count() > 0:
            for n in notifications.unread_notifications.all():
                notifications.unread_notifications.remove(n)
                notifications.read_notifications.add(n)
        objects = notifications.read_notifications.all()
        context["notifications"] = objects[y:x]
        return render(request, "notifications/notifications-queryset.html", context)
    else:
        return nothing_html
