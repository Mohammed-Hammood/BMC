import html
import json
from itertools import chain
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from account.forms import LoginForm
from book.forms import BookForm, BookCommentForm, TagsForm, CategoryForm
from account.models import ProfileModel
from book.models import BookModel, BookCommentModel, BookTagsModel, SpreadsheetModel, LectureModel, DoctorModel
from notifications.models import NotificationModel, UserNotificationModel
from datetime import datetime, timedelta, timezone

from notifications.signals import notification
from tools.categories import book_category

nothing_json = HttpResponse(json.dumps("None"), content_type="application/json")
nothing_html = HttpResponse(html.escape("None"), content_type="application/html")


context = {
    "comparing_time": datetime.date(datetime.now()) - timedelta(days=3),
    "users": User.objects.all(),
    "profiles": ProfileModel.objects.all(),
    "category_form": CategoryForm,
    "books": BookModel.objects.all(),
    "book_tags": BookTagsModel.objects.all(),
    "book_form": BookForm(None),
    "tags_form": TagsForm(None),
    "login_form": LoginForm(None),
    "comment_form": BookCommentForm(None),
    "book_comments": BookCommentModel.objects.all(),
}


def get_authenticated_user_objects(request):
    context['liked_audios'] = BookModel.objects.filter(like=request.user)
    context['liked_books'] = BookModel.objects.filter(like=request.user)
    unread_notifications = get_object_or_404(UserNotificationModel, user=request.user).unread_notifications.all()
    read_notifications = get_object_or_404(UserNotificationModel, user=request.user).read_notifications.all()
    context["total_notifications"] = unread_notifications.count() + read_notifications.count()
    if unread_notifications.count() > 99:
        context["unread_notifications"] = "99+"
    else:
        context["unread_notifications"] = unread_notifications.count()
    if unread_notifications.count() > 0:
        context["notifications"] = unread_notifications[:15]
    else:
        context["notifications"] = read_notifications[:5]
    context['users'] = User.objects.exclude(id=request.user.id)
    context['user_profile'] = get_object_or_404(ProfileModel, user=request.user)
    return context


def get_session_objects(request):
    return context


def get_cookies_objects_(request, template_name, cookie_name, cookie_value):
        key = str(cookie_name)
        value = str(cookie_value)
        if key in request.COOKIES:
            request.COOKIES[key] = value
            cookie = request.COOKIES[key]
        else:
            request.COOKIES[key] = value
            cookie = request.COOKIES[key]
        context['cookie'] = cookie
        response = render(request, template_name, context)
        response.set_cookie(key, cookie)
        return response


def get_cookies_objects(request):
    if "share_sections" in request.COOKIES:
        share_sections = request.COOKIES.get("share_sections")
        context["share_sections"] = share_sections
    return context


def general_comment_add(request):
    parent_slug = request.POST.get('parent_slug')
    type = request.POST.get("type")
    comment = request.POST.get("comment")
    user = request.user
    if comment.strip() == '':
        return nothing_html
    if request.is_ajax() and request.method == 'POST' and user.is_authenticated and parent_slug is not None:
        obj = get_object_or_404(BookModel, slug=parent_slug)
        model = BookCommentModel(book=obj , comment=comment, user=user)
        model.save()
        comment = get_object_or_404(BookCommentModel, pk=model.pk)
        context['comment'] = comment
        context['object'] = obj
        return render(request, 'general/general_comments_base_container.html', context)
    else:
        raise nothing_html


def object_like_toggle(request):
    parent_slug = request.GET.get("parent_slug")
    type = request.GET.get("type")
    nothing = HttpResponse(json.dumps("None"), content_type="application/json")
    model = BookModel
    user = request.user
    if request.is_ajax() and user.is_authenticated and parent_slug is not None:
        obj = get_object_or_404(model, slug=parent_slug)
        data = {}
        if user not in obj.like.all():
            obj.like.add(user)
            data['dislike_color'] = 'black'
            data['like_color'] = 'blue'
            if user in obj.dislike.all():
                obj.dislike.remove(user)
        else:
            obj.like.remove(user)
            data['dislike_color'] = 'black'
            data['like_color'] = 'black'
            if user in obj.dislike.all():
                obj.dislike.remove(user)
        data['dislike_count'] = obj.dislike.count()
        data['like_count'] = obj.like.count()
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return nothing


def object_dislike_toggle(request):
    parent_slug = request.GET.get("parent_slug")
    type = request.GET.get("type")
    nothing = HttpResponse(json.dumps("None"), content_type="application/json")
    model = BookModel
    user = request.user
    if request.is_ajax() and user.is_authenticated and parent_slug is not None:
        obj = get_object_or_404(model, slug=parent_slug)
        data = {}
        if user not in obj.dislike.all():
            obj.dislike.add(user)
            data['like_color'] = 'black'
            data['dislike_color'] = 'blue'
            if user in obj.like.all():
                obj.like.remove(user)
        else:
            obj.dislike.remove(user)
            data['like_color'] = 'black'
            data['dislike_color'] = 'black'
            if user in obj.like.all():
                obj.like.remove(user)
        data['dislike_count'] = obj.dislike.count()
        data['like_count'] = obj.like.count()
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return nothing


def get_comments_count(request):
    slug = request.POST.get('parent_slug')
    type = request.POST.get('type')
    nothing = HttpResponse(json.dumps("None"), content_type="application/json")
    if request.is_ajax() and request.method == 'POST':
        counts = get_object_or_404(BookModel, slug=slug).comments.count()
        return HttpResponse(json.dumps(counts), content_type='application/json')
    else:
        return nothing_json


def general_comment_like_toggle(request):
    comment_slug = request.GET.get("comment_slug")
    type_ = request.GET.get('type')
    nothing = HttpResponse(json.dumps("None"), content_type="application/json")
    model = BookCommentModel
    user = request.user
    if request.is_ajax() and user.is_authenticated and comment_slug is not None:
        comment = get_object_or_404(model, slug=comment_slug)
        data = {}
        if user not in comment.like.all():
            comment.like.add(user)
            data['dislike_color'] = 'black'
            data['like_color'] = 'blue'
            if user in comment.dislike.all():
                comment.dislike.remove(user)
        else:
            comment.like.remove(user)
            data['dislike_color'] = 'black'
            data['like_color'] = 'black'
            if user in comment.dislike.all():
                comment.dislike.remove(user)
        data['dislike_count'] = comment.dislike.count()
        data['like_count'] = comment.like.count()
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return nothing


def general_comment_dislike_toggle(request):
    comment_slug = request.GET.get("comment_slug")
    type_ = request.GET.get('type')
    nothing = HttpResponse(json.dumps("None"), content_type="application/json")
    model = BookCommentModel
    user = request.user
    if request.is_ajax() and user.is_authenticated and comment_slug is not None:
        comment = get_object_or_404(model, slug=comment_slug)
        data = {}
        if user not in comment.dislike.all():
            comment.dislike.add(user)
            data['dislike_color'] = 'blue'
            data['like_color'] = 'black'
            if user in comment.like.all():
                comment.like.remove(user)
        else:
            comment.dislike.remove(user)
            data['dislike_color'] = 'black'
            data['like_color'] = 'black'
            if user in comment.like.all():
                comment.like.remove(user)
        data['dislike_count'] = comment.dislike.count()
        data['like_count'] = comment.like.count()
        return HttpResponse(json.dumps(data), content_type='application/json',)
    else:
        return nothing


def general_comment_delete(request):
    comment_slug = request.POST.get('comment_slug')
    type_ = request.POST.get('type')
    nothing = HttpResponse(json.dumps("None"), content_type="application/json")
    if request.is_ajax() and request.method == 'POST' and type_ is not None and comment_slug is not None:
        comment = get_object_or_404(BookCommentModel, slug=comment_slug)
        if comment.user != request.user or comment.book.user != request.user:
            return nothing
        comment.delete()
        return HttpResponse(json.dumps('deleted'), content_type='application/json')
    else:
        return nothing_json


def general_comments_sort_or_load(request):
    type = request.POST.get("type", None)
    number = request.POST.get("number")
    slug = request.POST.get("parent_slug", None)
    if slug is None:
        return nothing_html
    if "general-comments-load" in request.path:
        y = int(number)
        x = y + 5
    else:
        x = int(number)
        y = 0
    if request.is_ajax() and request.method == "POST" and type is not None:
        sort = request.POST.get("sort")
        if sort == "0":
            ordering = "-id"
        elif sort == "1":
            ordering = "id"
        elif sort == "2":
            ordering = "-like"
        else:
            ordering = '-dislike'
        comments = BookCommentModel.objects.filter(book__slug=slug).order_by(ordering)[y:x]
        context["comments"] = comments
        return render(request, 'general/comments-queryset.html', context)
    else:
        return nothing_html


def objects_loader(request):
    query = request.POST.get("searchValue", None)
    category = request.POST.get('c', 'General')
    tag = request.POST.get('tag', None)
    filter = request.POST.get('filter', None)
    type = request.POST.get("type")
    count = request.POST.get("objectsCount")
    parent_slug = request.POST.get("parent_slug")
    load_count = request.POST.get("loadCount", None)
    if load_count is not None and int(load_count) > 0:
        increment = int(load_count)
    else:
        increment = 3
    if int(count) < 0:
        count = 0
    y = int(count)
    x = y + increment
    if request.is_ajax() and request.method == "POST":
        model = BookModel
        context_name = "books"
        template_name = "book/includes/books-loader.html"
        objects = model.objects.all().order_by("-id")
        if query and str(query).strip != "":
            objects = model.manager.search(query=query, category=category)
        if tag and str(tag).strip() != "":
            objects = model.objects.filter(tags__slug__icontains=tag)
        if filter and str(filter).strip() != "":
            if filter == "like":
                objects = model.objects.filter(like=request.user)
            elif filter == "dislike":
                objects = model.objects.filter(dislike=request.user)
            elif filter == "a":
                qs = User.objects.filter(username__exact=parent_slug).exists()
                if qs:
                    uploader = get_object_or_404(User, username=parent_slug)
                    objects = model.objects.filter(user=uploader)
            elif filter == "p":
                template_name = "registration/uploader-queryset.html"
                objects = ProfileModel.objects.all().order_by("id")
                context_name = "profiles"
                if query and query.strip != "":
                    objects = ProfileModel.manager.search(query=query)
            elif filter == "cy":
                template_name = "book/includes/books-loader.html"
                objects = BookModel.objects.filter(category=parent_slug)
                context_name = "books"
                if query and query.strip != "":
                    objects = BookModel.manager.search(query=query, category=parent_slug)
            else:
                template_name = "book/includes/books-loader.html"
                context_name = "books"
                objects = BookModel.objects.all().order_by("-id")
                if query and query.strip != "":
                    objects = BookModel.manager.search(query=query, category=parent_slug)
                else:
                    pass
        context["total_objects"] = objects.count()
        context['objects'] = objects[y:x]
        context['%s' % context_name] = objects[y:x]
        return render(request, template_name, context)
    else:
        return nothing_html


def get_comment_form(request, slug=None):
    comment_slug = request.POST.get('comment_slug')
    type_ = request.POST.get('type')
    nothing = HttpResponse(json.dumps("None"), content_type="application/json")
    if type_ == 'bk':
        model = BookCommentModel
        comment = get_object_or_404(model, slug=comment_slug)
        form = BookCommentForm(instance=comment)
    else:
        return nothing
    if request.is_ajax() and comment_slug is not None and request.method == 'POST':
        if request.user != comment.user:
            return nothing
        context['general_comment_form'] = form
        context['comment'] = comment
        return render(request, 'general/general-comment-form.html', context)
    else:
        return nothing


def save_comment_update(request, slug=None):
    new_comment = request.POST.get('comment')
    comment_slug = request.POST.get('comment_slug')
    type_ = request.POST.get('type')
    if type_ == 'bk':
        model = BookCommentModel
    else:
        return nothing_json
    if request.is_ajax() and comment_slug is not None and request.method == 'POST' and get_object_or_404(model, slug=comment_slug).user == request.user:
        model.objects.filter(slug=comment_slug).update(comment=new_comment)
        context['comment'] = get_object_or_404(model, slug=comment_slug)
        return render(request, 'general/only_update_comment_container.html', context)
    else:
        return nothing_html


def tags_create(request):
    tag = request.POST.get('tag')
    type = request.POST.get('type')
    if type == "bk":
        model = BookTagsModel
    else:
        return nothing_html
    if str(tag).strip() == "":
        return nothing_html
    slug = slugify(str(tag))
    user = request.user
    if request.is_ajax() and request.method == "POST" and user.is_authenticated:
        qs = model.objects.filter(slug__exact=slug).exists()
        if qs:
            context["tag"] = get_object_or_404(model, slug=slug)
            return render(request, 'general/tags-form-base-container.html', context)
        else:
            tag = model.objects.create(title=tag, user=user)
            context['tag'] = get_object_or_404(model, id=tag.id)
            return render(request, 'general/tags-form-base-container.html', context)
    else:
        return nothing_html


def add_tags_to_model(request, type, tags_count, parent_slug, operation="upload"):
    if type == "bk":
        parent_model = BookModel
        tag_model = BookTagsModel
    else:
        return nothing_json
    if request and type and tags_count and parent_slug:
        obj_qs = parent_model.objects.filter(slug=parent_slug).exists()
        if obj_qs:
            obj = get_object_or_404(parent_model, slug=parent_slug)
            if operation == "update":
                for old_tag in obj.tags.all():
                    obj.tags.remove(old_tag)
            for x in range(tags_count):
                t_slug = request.POST.get("tag_"+str(x))
                tag_slug = str(t_slug).strip()
                qs = tag_model.objects.filter(slug=tag_slug).exists()
                if qs:
                    tag = get_object_or_404(tag_model, slug=tag_slug)
                    if tag in obj.tags.all():
                        pass
                    else:
                        obj.tags.add(tag)
                else:
                    pass
        return HttpResponse(json.dumps("saved"), content_type="application/json")
    else:
        return nothing_json


def object_download_count_increment(request):
    parent_slug = request.POST.get("parent_slug", None)
    type = request.POST.get("type")
    if parent_slug is not None and request.is_ajax() and request.method == "POST":
        if type == "bk":
            model = BookModel
        else:
            return nothing_json
        qs = model.objects.filter(slug=parent_slug).exists()
        if qs:
            obj = model.objects.filter(slug=parent_slug).update(download=F('download') + 1)
            return HttpResponse(json.dumps("saved"), content_type="application/json")
    else:
        return nothing_json


def object_views_count_increment(request):
    slug = request.POST.get("parent_slug")
    type = request.POST.get("type")
    if slug and type:
        if type == "bk":
            model = BookModel
        elif type == "st":
            model = SpreadsheetModel
        elif type == "lr":
            model = LectureModel
            qs = model.objects.filter(id=slug).exists()
            if qs:
                obj = model.objects.filter(id=slug).update(views=F('views') + 1)
                return HttpResponse(json.dumps('save'), content_type="application/json")
        else:
            return nothing_json
        qs = model.objects.filter(slug=slug).exists()
        if qs:
            obj = model.objects.filter(slug=slug).update(views=F('views') + 1)
            return HttpResponse(json.dumps('save'), content_type="application/json")
    else:
        return nothing_json


def tags_views_count_increment(request):
    slug = request.POST.get("tag_slug")
    type = request.POST.get("type")
    if slug and type:
        if type == "bk":
            model = BookTagsModel
        else:
            return nothing_json
        qs = model.objects.filter(slug=slug).exists()
        if qs:
            obj = model.objects.filter(slug=slug).update(views=F('views') + 1)
            return HttpResponse(json.dumps('save'), content_type="application/json")
    else:
        return nothing_json


def uploader_follow_toggle(request):
    user = request.user
    if user.is_authenticated and request.method == "POST":
        user_id = request.POST.get("uploader")
        qs = ProfileModel.objects.filter(user__id=user_id).exists()
        if qs:
            uploader = get_object_or_404(ProfileModel, user__id=user_id)
            if user == uploader.user:
                return nothing_json
            if user in uploader.follow.all():
                uploader.follow.remove(user)
                btn_class = "btn btn-dark responsive-square-120 responsive-text-15"
                text_status = "Follow"
            else:
                uploader.follow.add(user)
                notification(
                    type="follow",
                    user=request.user,
                    link= get_object_or_404(ProfileModel, user=request.user).get_absolute_url(),
                    message="now is following you",
                    target_content_object=uploader.user,
                    actor_content_object=request.user,
                )
                btn_class = "btn btn-light responsive-square-120 responsive-text-15"
                text_status = "UnFollow"
            follow_count = uploader.follow.count()
            data = {
                "count": follow_count,
                "class": btn_class,
                "textStatus": text_status,
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return nothing_json
    else:
        return nothing_json


def create_spreadsheet(request):
    title = request.POST.get('title')
    if str(title).strip() == "":
        return nothing_html
    user = request.user
    if request.is_ajax() and user.is_authenticated and request.method == "POST":
            spreadsheet = SpreadsheetModel.objects.create(title=title, user=user,)
            context['object'] = get_object_or_404(SpreadsheetModel, id=spreadsheet.id)
            return render(request, 'book/includes/single-spreadsheet-base-container.html', context)
    else:
        return nothing_html


def spreadsheets_loader(request):
    loaded_objects = request.POST.get('loaded_objects')
    search = request.POST.get('search')
    material = request.POST.get('material')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    type = request.POST.get("type")
    parent_slug = request.POST.get("parent_slug")
    y = int(loaded_objects)
    x = y + 10
    if request.is_ajax() and request.method == "POST":
        print('pass 1')
        if type == "st":
            qs = User.objects.filter(username__exact=parent_slug).exists()
            if qs is False:
                return nothing_html
            model = SpreadsheetModel
            context_name = "spreadsheets"
            template_name = "book/includes/spreadsheets-queryset.html"
            objects = model.objects.filter(user__username=parent_slug).order_by("-id")
        elif type == "lr-by-dr":
            print('pass lr-by-dr')
            qs = DoctorModel.objects.filter(id=parent_slug).exists()
            if qs is False:
                return nothing_html
            context_name = "lectures"
            template_name = "book/includes/lectures-queryset.html"
            doctor = get_object_or_404(DoctorModel, id=parent_slug)
            objects = doctor.lectures.all().order_by("-id")
        elif type == "lr":
            print('pass 2')
            qs = SpreadsheetModel.objects.filter(slug=parent_slug).exists()
            if qs is False:
                return nothing_html
            context_name = "lectures"
            template_name = "book/includes/lectures-queryset.html"
            spreadsheet = get_object_or_404(SpreadsheetModel, slug=parent_slug)
            objects = spreadsheet.lectures.all().order_by("-id")
            if search and search.strip != "":

                objects = spreadsheet.lectures.model.manager.search(query=search).order_by("-id")
            if material and start_date and end_date:
                print('pass 3 material')
                objects = spreadsheet.lectures.model.manager.filter_by_date(
                    material=material, to_date=start_date, from_date=end_date
                ).order_by("-id")
                print('obj: ', objects.count())
        else:
            return nothing_html
        print('pass final')
        context['objects'] = objects[y:x]
        context['%s' % context_name] = objects[y:x]
        return render(request, template_name, context)
    else:
        return nothing_html


def contributors_toggle(request):
    user = request.user
    if request.is_ajax() and user.is_authenticated and request.method == "POST":
        contributor_username = request.POST.get("contributor")
        spreadsheet_slug = request.POST.get("spreadsheet_slug")
        type = request.POST.get("type")
        user_qs = User.objects.filter(username__exact=contributor_username).exists()
        spreadsheet_qs = SpreadsheetModel.objects.filter(slug__exact=spreadsheet_slug).exists()
        if user_qs and spreadsheet_qs:
            contributor = get_object_or_404(User, username__exact=contributor_username)
            spreadsheet = get_object_or_404(SpreadsheetModel, slug__exact=spreadsheet_slug)
            if user != spreadsheet.user:
                return nothing_html
            if type == "remove":
                if contributor in spreadsheet.contributors.all():
                    spreadsheet.contributors.remove(contributor)
            elif type == "add":
                if contributor not in spreadsheet.contributors.all():
                    spreadsheet.contributors.add(contributor)
            else:
                return nothing_html
            context['spreadsheet'] = spreadsheet
            return render(request, 'book/includes/contributors-container.html', context)
        else:
            return nothing_html
    else:
        return nothing_html