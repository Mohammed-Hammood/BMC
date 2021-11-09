from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from tools.categories import book_category, general_category, material_list
from tools.unique_url import random_unique_chars_digit_slug_generator
from datetime import datetime, time, timedelta, date


class CommentsManager(models.Manager):
    def sliced(self):
        return super(CommentsManager, self).all()[:5]


class BookManager(models.Manager):
    def search(self, query, category=None, type=None):
        if query and category == "General":
            qs = super(BookManager, self).filter(
                Q(description__icontains=query) |
                # Q(tags__icontains=query) |
                Q(title__icontains=query) |
                Q(user__username__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__contains=query)
            ).distinct()
            return qs
        elif query is not None and category != 'General':

            qs = super(BookManager, self).filter(
                Q(description__icontains=query) and Q(category__contains=category) |
                Q(tags__icontains=query) and Q(category__contains=category) |
                Q(title__icontains=query) and Q(category__contains=category) |
                Q(user__username__icontains=query) and Q(category__contains=category) |
                Q(user__first_name__icontains=query) and Q(category__contains=category) |
                Q(user__last_name__icontains=query)and Q(category__contains=category)
            ).distinct()
            return qs
        else:
            return None


class LectureManager(models.Manager):
    def search(self, query, material="General"):
        if query and material == "General":
            qs = super(LectureManager, self).filter(
                Q(comment__icontains=query) |
                Q(title__icontains=query) |
                Q(doctor__icontains=query) |
                Q(links__title__icontains=query)
            ).distinct()
            return qs

        elif query is not None and material != 'General':
            qs = super(LectureManager, self).filter(
                Q(comment__icontains=query) and Q(material__contains=material) |
                Q(title__icontains=query) and Q(material__contains=material) |
                Q(doctor__icontains=query) and Q(material__contains=material) |
                Q(links__title__icontains=query) and Q(material__contains=material)
            ).distinct()
            return qs
        else:
            return None

    def filter_by_date(self, material, from_date, to_date, *args, **kwargs):
        if material and from_date and to_date:

            s_year, s_month, s_day = from_date.split("-")
            e_year, e_month, e_day = to_date.split("-")
            start_date = datetime.combine(date(int(s_year), int(s_month), int(s_day)), time())
            end_date = datetime.combine(date(int(e_year), int(e_month), int(e_day)), time())
            qs = super(LectureManager, self).filter(timestamp__range=(start_date, end_date)).filter(
                material__exact=material
            )
            print("filter by date", qs)
            return qs
        else:
            pass


class BookTagsModel(models.Model):
    title = models.CharField(max_length=150, unique=False, db_index=True)
    slug = models.SlugField(_('Slug'), max_length=255, blank=True, unique=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    views = models.BigIntegerField(default=0, blank=True, null=True)
    type = models.CharField(max_length=10, null=True, blank=True, default="bk")
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        super(BookTagsModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_app:tags-view", kwargs={"slug": self.slug})


class BookModel(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    slug = models.SlugField(blank=True, editable=False, unique=True)
    like = models.ManyToManyField(User, related_name='book_likes', blank=True)
    dislike = models.ManyToManyField(User, related_name='book_dislike', blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='books/cover')
    thumbnail_cdn = models.TextField(null=True, blank=True)
    file = models.FileField(blank=True, null=True, upload_to="books/pdf/")
    file_cdn = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=book_category, default='General')
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(BookTagsModel, related_name='tags', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # auto_now_add for creation date
    update = models.DateTimeField(auto_now=True)  # auto_now for update
    views = models.BigIntegerField(default=0, blank=True)
    share = models.BigIntegerField(default=0, blank=True)
    download = models.PositiveIntegerField(default=0, blank=True, null=True)
    download_link_1 = models.TextField(blank=True, null=True)
    download_link_2 = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=5, null=True, blank=True, default='bk')
    objects = models.Manager()
    manager = BookManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id', '-timestamp']

    def get_absolute_url(self):
        return reverse("book_app:book_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("book_app:book-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("book_app:book-delete", kwargs={"slug": self.slug})

    def get_profile_url(self):
        return reverse("account_app:profile", kwargs={'username': self.user.username})


class BookCommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentsmodel_set')
    slug = models.SlugField(blank=True, null=True, editable=False, unique=True)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=1000)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislikes', blank=True)
    type = models.CharField(max_length=5, null=True, blank=True, default='bk')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    objects = CommentsManager()

    def get_profile_url(self):
        return reverse("account_app:profile", kwargs={'username': self.user.username})


class SpreadsheetModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spreadsheets')
    slug = models.SlugField(blank=True, null=True, editable=False, unique=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    contributors = models.ManyToManyField(User, related_name='contributors', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    views = models.BigIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_profile_url(self):
        return reverse("account_app:profile", kwargs={'username': self.user.username})

    def get_absolute_url(self):
        return reverse("book_app:spreadsheet-detail", kwargs={'username': self.user.username, 'slug': self.slug})


doctor_img_cdn = (
    ("/static/img/cdn/doctor-male.jpg", "Male"), ("/static/img/cdn/doctor-female.jpg", "Female")
)


class DoctorModel(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225, blank=True, null=True)
    surname = models.CharField(max_length=225, blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    picture_cdn = models.CharField(choices=doctor_img_cdn, max_length=1000, blank=True, null=True)
    gender = models.CharField(choices=(("Male", "Male"), ("Female", "Female")), max_length=1000, default=1)
    description = models.TextField(max_length=1000, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    facebook = models.CharField(blank=True, null=True, max_length=10000)
    phone_no = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("book_app:doctor-detail", kwargs={"id": self.id})

    def __str__(self):
        if self.last_name:
            second_name = self.last_name
            if self.surname:
                second_name = self.last_name + ' ' + self.surname
        elif self.surname:
            second_name = self.surname
            if self.last_name:
                second_name = self.last_name + ' ' + self.surname
        else:
            second_name = ""
        full_name = self.first_name + ' ' + second_name
        return full_name


class LectureModel(models.Model):
    material = models.CharField(choices=material_list, default=material_list[0], max_length=100)
    doctor = models.ForeignKey(DoctorModel, related_name='lectures', on_delete=False)
    title = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='book/lecture/file/', blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    spreadsheet = models.ForeignKey(SpreadsheetModel, related_name='lectures', blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    views = models.BigIntegerField(default=0, blank=True, null=True)
    objects = models.Manager()
    manager = LectureManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_app:lecture-detail", kwargs={"slug": self.spreadsheet.slug, "lecture_id": self.id})



pre_save.connect(random_unique_chars_digit_slug_generator, sender=BookModel)
pre_save.connect(random_unique_chars_digit_slug_generator, sender=SpreadsheetModel)
pre_save.connect(random_unique_chars_digit_slug_generator, sender=BookCommentModel)