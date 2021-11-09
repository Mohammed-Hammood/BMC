from django.conf import settings
from django.conf.urls import url, include
from django.urls import path
from book import views
from tools import utils
app_name = 'book_app'

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name="home"),
    url(r'^book_view=(?P<slug>[-\w]+)$', views.book_detail, name='book_detail'),
    url(r'^tags=(?P<slug>[-\w]+)$', views.view_by_tags, name='tags-view'),
    url(r'^category=(?P<category>[-\w]+)$', views.view_by_category, name='categories-view'),
    url(r'^book_view=(?P<slug>[-\w]+)/d/$', views.book_delete, name='book-delete'),
    url(r'^book_view=(?P<slug>[-\w]+)/e/$', views.book_edit, name='book-update'),
    url(r'^ajax-book-update/$', views.book_edit, name='ajax-book-update'),
    url(r'^liked_books$', views.liked_books, name='liked-books'),
    url(r'^upload$', views.book_upload, name='book-upload'),

    url(r'^change-thumbnail/$', views.book_cover_update, name='change-thumbnail'),
    url(r'^change-thumbnail/$', views.book_cover_update, name='change-thumbnail'),
    url(r'^general-object-delete/$', views.book_delete, name="general-object-delete"),
    url(r'^object-like-toggle/$', utils.object_like_toggle, name="object-like-toggle"),
    url(r'^object-dislike-toggle/$', utils.object_dislike_toggle, name="object-dislike-toggle"),
    url(r'^general-objects-loader/$', utils.objects_loader, name="general-objects-loader"),

    url(r'^comment-like-toggle/$', utils.general_comment_like_toggle, name='comment-like-toggle'),
    url(r'^comment-dislike-toggle/$', utils.general_comment_dislike_toggle, name='comment-dislike-toggle'),
    url(r'^general-comment-delete/$', utils.general_comment_delete, name='general-comment-delete'),
    url(r'^get-comment-form/$', utils.get_comment_form, name='get-comment-form'),
    url(r'^save-comment-changes/$', utils.save_comment_update, name='save-comment-changes'),
    url(r'^comment-counts/$', utils.get_comments_count, name='comments-count'),
    url(r'^general-comment-add/$', utils.general_comment_add, name='general-comment-add'),
    url(r'^general-comments-sorts/$', utils.general_comments_sort_or_load, name='general-comments-sort'),
    url(r'^general-comments-load/$', utils.general_comments_sort_or_load, name='general-comments-load'),

    url(r'^o-d-i/$', utils.object_download_count_increment, name='download-increment'),
    url(r'^o-v-i/$', utils.object_views_count_increment, name='views-increment'),
    url(r'^t-v-i/$', utils.tags_views_count_increment, name='tags-views-inc'),
    url(r'^tags-create/$', utils.tags_create, name="tags-create"),
    url(r'^add-tags-model/$', utils.add_tags_to_model, name="tags-to-model"),
    url(r'^u-f-t/$', utils.uploader_follow_toggle, name="uploader-follow-toggle"),

    url(r'^c-n-sp-sh/$', utils.create_spreadsheet, name="create-spreadsheet"),
    url(r'^spreadsheets-loader/$', utils.spreadsheets_loader, name="spreadsheets-loader"),
    url(r'^contributors-toggle/$', utils.contributors_toggle, name="contributors-toggle"),

    url(r'^(?P<username>[-\w]+)/spreadsheet=(?P<slug>[-\w]+)$', views.spreadsheet_detail, name='spreadsheet-detail'),
    url(r'^spreadsheet=(?P<slug>[-\w]+)/del/$', views.spreadsheet_delete, name='spreadsheet-delete'),
    url(r'^spreadsheet=(?P<slug>[-\w]+)/edit/$', views.spreadsheet_edit, name='spreadsheet-edit'),
    url(r'^(?P<username>[-\w]+)/spreadsheets$', views.spreadsheets_view, name='spreadsheets'),

    url(r'^spreadsheet=(?P<slug>[-\w]+)/lecture=(?P<lecture_id>[0-9]+)$', views.lecture_detail, name='lecture-detail'),
    url(r'^lecture=(?P<id>[0-9]+)/edit/$', views.lecture_edit, name='lecture-edit'),
    url(r'^lecture=(?P<id>[0-9]+)/del/$', views.lecture_delete, name='lecture-delete'),
    url(r'^lecture-create-ajax$', views.create_lecture, name='lecture-create'),

    url(r'^doctor/id=(?P<id>[0-9]+)/$', views.doctor_detail, name='doctor-detail'),

]
