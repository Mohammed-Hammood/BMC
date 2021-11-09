from django.contrib import admin
from .models import ProfileModel


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'country', 'city', 'phone_no']
    list_display_links = ['id','user', 'country', 'city', 'phone_no']
    search_fields = ['user', 'country', 'city']
    readonly_fields = ['update', 'timestamp']
    list_filter = ['user', 'country', 'city']

    class Meta:
        model = ProfileModel


admin.site.register(ProfileModel, ProfileAdmin)
