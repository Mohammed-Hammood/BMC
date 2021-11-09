from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from tools.categories import book_category
from tools.validators import valid_file_extension, valid_file_mimetype, valid_lecture_extension, valid_lecture_mimetype
from .models import BookModel, BookCommentModel, BookTagsModel, LectureModel, SpreadsheetModel


class BookUpdateForm(forms.ModelForm):

    class Meta:
        model = BookModel
        fields = ['title', 'description', 'file_cdn', 'thumbnail', 'thumbnail_cdn', 'download_link_1', 'download_link_2', 'category']

        widgets = {
            "description": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;display:block;z-index:0;",
                "placeholder": _("Describe your book"),
            }),
            "file_cdn": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Book url"),
                "autofocus": True,
            }),
            "download_link_1": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Download link 1 (optional)"),
            }),
            "download_link_2": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Download link 2 (optional)"),
            }),
            "thumbnail_cdn": forms.Textarea(attrs={
                "class": "form-control responsive-text-15",
                "style": "height:150px;display:block;z-index:0;",
                "placeholder": _("Book cover url (optional)"),
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control responsive-text-15",
                'placeholder': "Title",
                "style": "display:block;z-index:0;",
            }),
            "category": forms.Select(attrs={
                "class": "form-control responsive-text-15",
                "style": "z-index:0;",
            }),
        }
        labels = {
            "thumbnail": _("Cover"),
            "thumbnail_cdn": _("Cover url"),
            "file_cdn": _("Book url"),
            "title": _("Title"),
        }

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")
        if thumbnail:
            img = str(thumbnail).lower()
            if not valid_file_mimetype(img, "image") or not valid_file_extension(img, "image"):
                raise ValidationError(_('Please enter a valid image'))
            else:
                return thumbnail


class BookForm(forms.ModelForm):

    class Meta:
        model = BookModel
        fields = [
            'title', 'file', 'file_cdn', 'description', 'download_link_1',
            'download_link_2', 'thumbnail', 'thumbnail_cdn', 'category']
        labels = {
            "thumbnail": _("Cover"),
            "thumbnail_cdn": _("Cover url"),
            "file_cdn": _("Book url"),
            "title": _("Title"),
        }
        widgets = {
            "description": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Describe your book"),
            }),
            "file_cdn": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Book url"),
                "autofocus": True,
            }),
            "file":forms.FileInput(attrs={
                "class": "form-control responsive-text-15",
                "accept": "application/pdf",
                "onchange": "getFileName(event)",
                "style": "z-index:0;",
            }),
            "thumbnail_cdn": forms.Textarea(attrs={
                "class": "form-control responsive-text-15",
                "style": "height:150px;display:block;z-index:0;",
                "placeholder": _("Book cover url (optional)"),
            }),
            "download_link_1": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Download link 1 (optional)"),
            }),
            "download_link_2": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Download link 2 (optional)"),
            }),
            "thumbnail":forms.FileInput(attrs={
                "class": "form-control responsive-text-15",
                "accept": "image/jpeg, image/jpg, image/png",
                "style": "z-index:0;",
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control responsive-text-15",
                'placeholder': _("Title"),
                "style": "z-index:0;",
            }),
            "category": forms.Select(attrs={
                "class": "form-control responsive-text-15",
                "style": "z-index:0;",
            }),
        }

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")
        if thumbnail:
            img = str(thumbnail).lower()
            if not valid_file_mimetype(img, "image") or not valid_file_extension(img, "image"):
                raise ValidationError(_('Please enter a valid image'))
            else:
                return thumbnail

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            f = str(file).lower()
            if not valid_file_extension(f, "book") or not valid_file_mimetype(f, "book"):
                raise ValidationError(_('Please upload a valid book'))
            else:
                return file
        else:
            pass


class LectureForm(forms.ModelForm):

    class Meta:
        model = LectureModel
        fields = ['title', 'material', 'doctor', 'file', 'comment']
        labels = {
            "material": _("Material"),
            "title": _("Title"),
            "file": _("Lecture File (optional)"),
            "download_links": _("download links (optional)"),
        }
        widgets = {
            "comment": forms.Textarea(attrs={
                "class": 'form-control responsive-text-15',
                "style": "height:150px;z-index:0;",
                "placeholder": _("Comment (optional)"),
            }),
            "material": forms.Select(attrs={
                "class": "form-control responsive-text-15",
                "style": "display:block;z-index:0;",
            }),
            "doctor": forms.Select(attrs={
                "class": "form-control responsive-text-15",
                "style": "display:block;z-index:0;",
            }),
            "file": forms.FileInput(attrs={
                "class": "form-control responsive-text-15",
                "accept": "application/pdf, application/x-rar-compressed, application/zip, application/msword, "
                          "application/vnd.openxmlformats-officedocument.wordprocessingml.document, "
                          "application/vnd.ms-powerpoint,"
                          "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "style": "z-index:0;",
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control responsive-text-15",
                'placeholder': _("Title"),
                "style": "z-index:0;",
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            f = str(file).lower()
            if not valid_lecture_extension(f) or not valid_lecture_mimetype(f):
                raise ValidationError(_('Please upload a valid file'))
            else:
                return file
        else:
            pass


class BookCommentForm(forms.ModelForm):

    class Meta:
        model = BookCommentModel
        fields = ['comment']
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    'style': 'width:100%; height:100px; border-radius:10px;max-height:500px;',
                    'id': 'comment_id',
                    "required": True,
                    "placeholder": "Write a comment",
                }
            )
        }


class TagsForm(forms.Form):
    title = forms.CharField(
        max_length=35,
        label=_("Tags"),
        min_length="1",
        required=False,
        widget=forms.Textarea(attrs={
            "id": "tag_input_id",
            "class": "form-control responsive-text-15",
            "placeholder": _("Tags"),
            "style": "height:50px;",
        })
    )


class CategoryForm(forms.Form):
    c = forms.ChoiceField(
        choices=book_category,
        label='',
        widget=forms.Select(attrs={
            "class": "form-control responsive-text-15",
        }),
    )


class SpreadsheetForm(forms.ModelForm):

    class Meta:
        model = SpreadsheetModel

        fields = ['title', 'description']
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": _("Title"),
                "class": "form-control responsive-text-15",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": _("Describe your spreadsheet"),
                "class": "form-control responsive-text-15",
            })
        }