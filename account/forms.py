from django import forms
from django.core.exceptions import ValidationError, EmptyResultSet
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.models import User
from .models import ProfileModel
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=3,
        help_text="Username should not more than 100 or less than 6 "
                  "characters. Letters, digits and @/./+/-/_ only allowed.",
        widget=forms.TextInput(
            attrs={"placeholder": _("Username"),
                   "class": "form-control responsive-text-15",
                   }))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Password"),
            "class": "form-control responsive-text-15",
        }),
        max_length=50,
        min_length=8,
        help_text=_("Password should not be less than 8 or more than 100 characters.")
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            print(user, ", User.")
            if not user:
                raise forms.ValidationError(_('Incorrect password or username'))
            if not user.is_active:
                raise forms.ValidationError(_('This user is not active'))
            #       if user.check_password(password):
            #         raise ValidationError('Incorrect Password')
        return super(LoginForm, self).clean(*args, **kwargs)


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control responsive-text-15',
                'placeholder': 'Write your username',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control responsive-text-15',
                'placeholder': 'Write your Password',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control responsive-text-15',
                'placeholder': 'Write your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control responsive-text-15',
                'placeholder': 'Write your last name',
            }),
        }

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     qs = User.objects.filter(email__exact=email).exists()
    #     if qs is True:
    #         raise forms.ValidationError(_('This email already exists.'))
    #     return email


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = ProfileModel
        fields = [
            'picture',
            'description',
            'city',
            'country',
            'phone_no',
        ]


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            "placeholder": _("New password"),
            "class": "form-control responsive-text-15",
        }),

        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": _("New password confirmation"),
            "class": "form-control responsive-text-15",
        }),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True,
            "placeholder": _("Old password"),
            "class": "form-control responsive-text-15",
        }),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
