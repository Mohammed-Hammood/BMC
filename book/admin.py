from django.contrib import admin
from .models import BookModel, BookTagsModel, BookCommentModel, SpreadsheetModel, LectureModel, DoctorModel


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'file_cdn', 'slug', 'category', 'timestamp']
    list_display_links = ['id', 'title', 'user', 'file_cdn', 'slug', 'category', 'timestamp']
    readonly_fields = ['slug', 'timestamp', 'update']

    class Meta:
        model = BookModel


class TagsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "timestamp", "update"]
    list_display_links = ["id", "title", "slug", "timestamp", "update"]
    search_fields = ["id", "title", "slug", "timestamp", "update"]
    readonly_fields = ["id", "title", "slug", "timestamp", "update"]

    class Meta:
        model = BookTagsModel


class BookCommentAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'comment', 'timestamp', 'update']
    list_display_links = ['id', 'user',  'comment', 'timestamp', 'update']
    readonly_fields = ['id', 'timestamp', 'update']

    class Meta:
        model = BookCommentModel


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'surname', 'birthday', 'email', 'phone_no']
    list_display_links = ['id','first_name', 'last_name', 'surname', 'birthday', 'email', 'phone_no']
    readonly_fields = ['timestamp', 'update']

    class Meta:
        model = DoctorModel


admin.site.register(BookModel, BookAdmin)
admin.site.register(BookTagsModel, TagsAdmin)
admin.site.register(BookCommentModel, BookCommentAdmin)
admin.site.register(LectureModel)
admin.site.register(SpreadsheetModel)
admin.site.register(DoctorModel, DoctorAdmin)