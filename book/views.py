import html
import json
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError, PermissionDenied, ViewDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, View, ListView
from account.models import ProfileModel
from book.forms import BookForm, BookUpdateForm, CategoryForm, LectureForm, SpreadsheetForm
from notifications.models import NotificationModel
from notifications.signals import notification
from tools.categories import book_category
from tools.utils import add_tags_to_model, context, get_authenticated_user_objects, get_session_objects
from tools.validators import valid_file_extension, valid_file_mimetype, valid_lecture_extension, valid_lecture_mimetype, \
    get_file_mimetype
from .models import BookModel, BookTagsModel, SpreadsheetModel, LectureModel, DoctorModel
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Page, Paginator, InvalidPage, EmptyPage
from django.db.models import F, Q
from .models import BookCommentModel
from urllib.parse import quote_plus
nothing_html = HttpResponse(html.escape("None"), content_type="application/json")
nothing_json = HttpResponse(json.dumps("None"), content_type="application/json")


class HomePage(View):
    def get(self, request):
        if request.user.is_authenticated:
            get_authenticated_user_objects(request)
        context['tags'] = BookTagsModel.objects.all().order_by("-views")[:30]
        query = request.GET.get('search', None)
        category = request.GET.get('c', 'all')
        books = BookModel.objects.all().order_by("-id")
        if query is not None:
            if query.strip() != "":
                books = BookModel.manager.search(query=query, category=category)
                context['result_count'] = books.count()
                context['selected'] = category
                context['search_query'] = query
            else:
                pass
        get_session_objects(request)
        context['total_objects'] = books.count()
        context['books'] = books[:5]
        return render(request, 'book/index.html', context)


def view_by_tags(request, slug):
    get_session_objects(request)
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    books = BookModel.objects.filter(tags__slug__icontains=slug)
    context['books'] = books[:5]
    context["total_objects"] = books.count()
    context['tags'] = BookTagsModel.objects.all().order_by("-views")[:30]
    return render(request, 'book/index.html', context)


def view_by_category(request, category):
    get_session_objects(request)
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    books = BookModel.objects.filter(category__icontains=category).order_by("-id")
    context['books'] = books[:5]
    context['tags'] = BookTagsModel.objects.all().order_by("-views")[:30]
    context['total_objects'] = books.count()
    return render(request, 'book/index.html', context)


def book_detail(request, slug=None, pk=None):
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    book = get_object_or_404(BookModel, slug=slug)
    context['book'] = book
    context['object'] = book
    context['share_string'] = quote_plus(book.description)
    context['profile'] = get_object_or_404(ProfileModel, user=book.user)
    context['comments'] = BookCommentModel.objects.filter(book__slug=slug).order_by('-id')[:5]
    context['profiles'] = ProfileModel.objects.all()
    return render(request,  'book/book-detail.html', context)


@login_required
def book_edit(request, slug=None, pk=None):
    if request.method == "POST" and request.is_ajax() and request.user.is_authenticated:
        title = request.POST.get("title")
        download_link_1 = request.POST.get('download_link_1')
        download_link_2 = request.POST.get('download_link_2')
        category = request.POST.get("category")
        file_cdn = request.POST.get('file_cdn')
        thumbnail_cdn = request.POST.get('thumbnail_cdn')
        description = request.POST.get("description")
        parent_slug = request.POST.get("parent_slug")
        if title and category and parent_slug:
            if str(title).strip == "" or str(category).strip == "" or str(parent_slug).strip() == "":
                return nothing_html
            qs = BookModel.objects.filter(slug=parent_slug).exists()
            if qs:
                model = get_object_or_404(BookModel, slug=parent_slug)
                model.title = title
                if description and str(description).strip != "":
                    model.description = description
                if file_cdn and file_cdn.strip() != "":
                    model.file_cdn = file_cdn
                if download_link_1 and download_link_1.strip() != "":
                    model.download_link_1 = download_link_1
                    model.save()
                if download_link_2 and download_link_2.strip() != "":
                    model.download_link_2 = download_link_2
                    model.save()
                if thumbnail_cdn and thumbnail_cdn.strip() != "":
                    model.thumbnail_cdn = thumbnail_cdn
                    model.save()
                model.category = category
                model.save()
                add_tags_to_model(request, "bk", 8, parent_slug, "update")
                context['book'] = get_object_or_404(BookModel, slug=parent_slug)
                return render(request, "book/includes/single-book-base-container.html", context)
            return nothing_html
    else:
        book = get_object_or_404(BookModel, slug=slug)
        form = BookUpdateForm(instance=book)
        context['book'] = book
        context['book_form'] = form
        get_session_objects(request)
        get_authenticated_user_objects(request)
        return render(request, 'book/book-edit.html', context)


@login_required
def book_delete(request, slug, id=None):
    obj = get_object_or_404(BookModel, slug=slug)
    if request.user != obj.user:
        raise PermissionDenied
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect('/')
    context['book'] = obj
    get_session_objects(request)
    get_authenticated_user_objects(request)
    return render(request, 'book/book_delete.html', context)


@login_required
def book_upload(request):
    if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        file = request.FILES.get('file')
        file_cdn = request.POST.get('file_cdn')
        thumbnail_cdn = request.POST.get('thumbnail_cdn')
        download_link_1 = request.POST.get('download_link_1')
        download_link_2 = request.POST.get('download_link_2')
        description = request.POST.get('description', None)
        thumbnail = request.FILES.get('thumbnail')
        category = request.POST.get('category', 'General')
        if file:
            if not valid_file_extension(str(file), "book") or not valid_file_mimetype(str(file), "book"):
                return nothing_html
        if file_cdn and file_cdn.strip() == "":
            return nothing_html
        if title and category:
            if title.strip() == "" or category.strip() == "":
                return nothing_html
            if description and description.strip() == "":
                return nothing_html
            if thumbnail:
                if not valid_file_extension(str(thumbnail), "image") or not valid_file_mimetype(str(thumbnail), "image"):
                    return nothing_html
            book = BookModel.objects.create(
                title=title, description=description, thumbnail=thumbnail,
                category=category, user=request.user
            )
            notification(
                type="book",
                user=book.user,
                message="uploaded new book",
                link=book.get_absolute_url(),
                actor_content_object=request.user,
                target_content_object=book
            )
            if file:
                book.file = file
                book.save()
            if file_cdn:
                book.file_cdn = file_cdn
                book.save()
            if download_link_1 and download_link_1.strip() != "":
                book.download_link_1 = download_link_1
                book.save()
            if download_link_2 and download_link_2.strip() != "":
                book.download_link_2 = download_link_2
                book.save()
            if thumbnail_cdn and thumbnail_cdn.strip() != "":
                book.thumbnail_cdn = thumbnail_cdn
                book.save()
            add_tags_to_model(request, "bk", 8, book.slug, "upload")
            context['book'] = book
            context['object'] = book
            return render(request, 'book/includes/single-book-base-container.html', context)

        else:
            return nothing_html
    get_authenticated_user_objects(request)
    context['book_form'] = BookForm(None)
    context['object'] = ''
    # object need to be reset because previous views may pass tags appear in current view
    return render(request, 'book/book_upload.html', context)


@login_required
def liked_books(request):
    get_session_objects(request)
    get_authenticated_user_objects(request)
    books = BookModel.objects.filter(like=request.user)
    context['liked_books_count'] = books.count()
    context['liked_books'] = books[:5]
    context['total_objects'] = books.count
    return render(request, 'book/liked-books.html', context)


def book_cover_update(request):
    img = request.FILES.get("img")
    parent_slug = request.POST.get("parent_slug")
    type = request.POST.get("type")
    if request.is_ajax() and request.method == "POST" and request.user.is_authenticated:
        if BookModel.objects.filter(slug=parent_slug).exists():
            obj = BookModel.objects.get(slug=parent_slug)
            obj.thumbnail = img
            obj.save()
            img_src = get_object_or_404(BookModel, slug=parent_slug).thumbnail.url
            data = {"src": img_src}
            return HttpResponse(json.dumps(data), content_type="application/json")
    return nothing_json


def spreadsheets_view(request, username):
    context['profiles'] = ProfileModel.objects.all()
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    spreadsheets = SpreadsheetModel.objects.filter(user__username=username).order_by('-id')
    context['total_objects'] = spreadsheets.count()
    context['spreadsheets'] = spreadsheets[:10]
    context['profile'] = get_object_or_404(ProfileModel, user__username=username)
    return render(request, 'book/stylesheets.html', context)


def spreadsheet_detail(request, username, slug):
    spreadsheet = get_object_or_404(SpreadsheetModel, user__username=username, slug=slug)
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.spreadsheet = spreadsheet
            instance.save()
            return redirect(spreadsheet.get_absolute_url())
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    qs = request.GET.get("search", None)
    material = request.GET.get("material", None)
    from_date = request.GET.get("from", None)
    to_date = request.GET.get("to", None)
    lectures = spreadsheet.lectures.all().order_by('-id')
    total_objects = spreadsheet.lectures.count()
    if from_date is not None and to_date is not None and material is not None:
        lectures = spreadsheet.lectures.model.manager.filter_by_date(
            material=material, from_date=from_date, to_date=to_date
        ).order_by("-id")
    if qs is not None:
        lectures = spreadsheet.lectures.model.manager.search(query=qs).order_by("-id")
    context['spreadsheet'] = spreadsheet
    context['total_objects'] = total_objects
    context['lectures'] = lectures[:10]
    context['results_count'] = lectures.count()
    context['lecture_form'] = LectureForm(None)
    return render(request, 'book/spreadsheet-detail.html', context)


def lecture_detail(request, slug, lecture_id):
    spreadsheet = get_object_or_404(SpreadsheetModel, slug=slug)
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.spreadsheet = spreadsheet
            instance.save()
            return redirect(spreadsheet.get_absolute_url())
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    context['spreadsheet'] = spreadsheet
    lecture = get_object_or_404(LectureModel, id=lecture_id)
    context['object'] = lecture
    if lecture.file:
        context['file_mimetype'] = get_file_mimetype(str(lecture.file))
    return render(request, 'book/lecture-detail.html', context)


def lecture_edit(request, id):
    lecture = get_object_or_404(LectureModel, id=id)
    if request.user not in lecture.spreadsheet.contributors.all() and request.user != lecture.spreadsheet.user:
        raise PermissionDenied
    form = LectureForm(request.POST or None, request.FILES or None, instance=lecture)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.spreadsheet = lecture.spreadsheet
            instance.save()
            return redirect(lecture.get_absolute_url())
    get_authenticated_user_objects(request)
    context['lecture_form'] = form
    context['lecture'] = lecture
    return render(request, 'book/lecture-update.html', context)


def lecture_delete(request, id):
    lecture = get_object_or_404(LectureModel, id=id)
    if request.user != lecture.spreadsheet.user:
        raise PermissionDenied
    if request.method == 'POST':
        lecture.delete()
        return redirect(lecture.spreadsheet.get_absolute_url())
    get_authenticated_user_objects(request)
    context['object'] = lecture
    return render(request, 'book/lecture-delete.html', context)


def spreadsheet_delete(request, slug):
    spreadsheet = get_object_or_404(SpreadsheetModel, slug=slug)
    if request.user != spreadsheet.user:
        raise PermissionDenied
    if request.method == 'POST':
        spreadsheet.delete()
        return redirect("book_app:spreadsheets", username=spreadsheet.user.username)
    get_authenticated_user_objects(request)
    context['object'] = spreadsheet
    return render(request, 'book/spreadsheet-delete.html', context)


def spreadsheet_edit(request, slug):
    spreadsheet = get_object_or_404(SpreadsheetModel, slug=slug)
    if request.user != spreadsheet.user:
        raise PermissionDenied
    form = SpreadsheetForm(request.POST or None, request.FILES or None, instance=spreadsheet)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect(spreadsheet.get_absolute_url())
    get_authenticated_user_objects(request)
    context['spreadsheet'] = spreadsheet
    context['spreadsheet_form'] = form
    return render(request, 'book/spreadsheet-update.html', context)


def doctor_detail(request, id):
    doctor = get_object_or_404(DoctorModel, id=id)
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    context['doctor'] = doctor
    context['object'] = doctor
    context['lectures'] = doctor.lectures.all()[:5]
    context['total_objects'] = doctor.lectures.count()
    return render(request, 'book/doctor-detail.html', context)


@login_required
def create_lecture(request):
    if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        file = request.FILES.get('file')
        doctor_id = request.POST.get('doctor_id')
        material = request.POST.get('material')
        parent_slug = request.POST.get('parent_slug')
        lecture_id = request.POST.get('lecture_id', None)
        operation = request.POST.get('operation')
        comment = request.POST.get('comment', None)
        if file:
            if not valid_lecture_extension(str(file)) or not valid_lecture_mimetype(str(file)):
                return nothing_html
        if title and doctor_id:
            if title.strip() == "" or doctor_id.strip() == "":
                return nothing_html
            if parent_slug and parent_slug.strip() == "":
                return nothing_html
            spreadsheet_qs = SpreadsheetModel.objects.filter(slug=parent_slug).exists()
            doctor_qs = DoctorModel.objects.filter(id=int(doctor_id)).exists()
            if spreadsheet_qs and doctor_qs:
                spreadsheet = get_object_or_404(SpreadsheetModel, slug=parent_slug)
                doctor = get_object_or_404(DoctorModel, id=int(doctor_id))
                if operation == "u":
                    qs = LectureModel.objects.filter(id=lecture_id).exists()
                    if qs:
                        obj = LectureModel.objects.filter(id=lecture_id).update(
                            title=title, doctor=doctor, spreadsheet=spreadsheet, material=material
                        )
                        lecture = get_object_or_404(LectureModel, id=int(lecture_id))
                    else:
                        return nothing_html
                elif operation == "c":
                    lecture = LectureModel.objects.create(
                        title=title, doctor=doctor,
                        material=material, spreadsheet=spreadsheet
                    )
                    notification(
                        type="lecture",
                        user=request.user,
                        link=lecture.get_absolute_url(),
                        message="uploaded new lecture",
                        actor_content_object=lecture.spreadsheet,
                        target_content_object=lecture,
                    )
                else:
                    return nothing_html
                if file:
                    lecture.file = file
                    lecture.save()
                if comment and comment.strip() != "":
                    lecture.comment = comment
                    lecture.save()
                context['lecture'] = lecture
                context['object'] = lecture
                return render(request, 'book/includes/single-lecture-base-container.html', context)
        return nothing_html