from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.timesince import timesince
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ProfileManager(models.Manager):
    def search(self, query):
        if query:
            qs = ProfileModel.objects.filter(
                Q(user__username=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query)
            )
            return qs
        else:
            pass


class ProfileModel(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    picture = models.ImageField(verbose_name='Profile photo', upload_to='profile/image', blank=True)
    picture_cdn = models.CharField(
        verbose_name='Profile photo', max_length=1000, blank=True, null=True,
        default="/static/img/cdn/profile_thumbnail_min.png")
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=500, default='', blank=True)
    follow = models.ManyToManyField(User, related_name='follow', blank=True)
    phone_no = models.IntegerField(default=0, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    manager = ProfileManager()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("account_app:profile", kwargs={"username": self.user.username})

    def get_edit_url(self):
        return reverse("account_app:account-edit")


def create_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user_profile = ProfileModel.objects.create(user=kwargs['instance'])


post_save.connect(create_profile_for_new_user, sender=User)