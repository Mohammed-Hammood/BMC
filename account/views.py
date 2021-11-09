import json, html
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from account.models import ProfileModel
from book.models import BookModel, BookCommentModel
from account.forms import RegistrationForm, LoginForm, ProfileEditForm, UserChangeForm, PasswordChangeForm
from tools.utils import get_authenticated_user_objects, get_session_objects, context


class RegistrationView(View):
    def get(self, request):

        context['form'] = RegistrationForm(None)
        return render(request, 'registration/register.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            instance.set_password(password)
            instance.save()
            user = authenticate(password=password, username=username)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    profile = get_object_or_404(ProfileModel, user=request.user)
                    return redirect(profile.get_absolute_url())
        return render(request, 'registration/register.html', context)


@login_required
def account_edit(request):
    profile = get_object_or_404(ProfileModel, user=request.user)
    context['profile'] = profile
    user_form = UserChangeForm(instance=request.user, data=request.POST or None)
    context['user_form'] = user_form
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=profile)
    context['profile_form'] = profile_form
    if request.method == "POST":
        if user_form.is_valid():
            user_form.save()
            if profile_form.is_valid():
                profile_f = profile_form.save(commit=False)
                profile_f.user = request.user
                profile_f.save()
                return redirect(profile.get_absolute_url())
        return redirect("account_app:account-edit")
    get_authenticated_user_objects(request)
    get_session_objects(request)
    return render(request, 'registration/account-update.html', context)


@login_required
def account_delete(request):
    profile = ProfileModel.objects.get_or_create(user=request.user)
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.user.username)
            user.delete()
        except User.DoesNotExist:
            pass
        logout(request)
        return redirect("book_app:home")
    context['profile'] = profile
    return render(request, 'registration/account-delete.html', context)


@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        profile = get_object_or_404(ProfileModel, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=form.user)
            return redirect(profile.get_absolute_url())
        else:
            return redirect("account_app:password-change")
    else:
        context['form'] = PasswordChangeForm(user=request.user)
        get_authenticated_user_objects(request)
        get_session_objects(request)
        return render(request, 'registration/password-change.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(password=password, username=username)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    profile = get_object_or_404(ProfileModel, user=request.user)
                    return redirect(profile.get_absolute_url())
    context['login_form'] = form
    return render(request, 'registration/log-in.html', context)


def logout_view(request):
    logout(request)
    return redirect('account_app:login')


class ProfileView(View):
    def get(self, request, username):
        context['profile'] = get_object_or_404(ProfileModel, user__username=username)
        books = BookModel.objects.filter(user__username=username).order_by('-id')
        context['objects'] = books[:5]
        context['total_objects'] = books.count
        if request.user.is_authenticated:
            get_authenticated_user_objects(request)
        return render(request, 'registration/profile.html', context)


def uploaders_view(request):
    if request.user.is_authenticated:
        get_authenticated_user_objects(request)
    profiles = ProfileModel.objects.all()
    qs = request.GET.get("search", None)
    if qs is not None:
        profiles = ProfileModel.manager.search(query=qs)
    context['total_objects'] = profiles.count()
    context['profiles'] = profiles[:4]
    return render(request, 'registration/uploaders.html', context)
