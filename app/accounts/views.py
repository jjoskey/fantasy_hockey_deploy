from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from . import forms
from django.http import HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User
import random
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
# email = EmailMessage('Test', 'Test Testov Yo', to=['alexander.s.ilyin@gmail.com'])
# email.send()


def password_generator():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def success_signup(request):
    return render(request, 'accounts/signup_success.html')

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:success")
    template_name = "accounts/signup.html"


def get_team_name(request):
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            form.save()
            return redirect('play')

    else:
        form = forms.ProfileForm()

    return render(request, 'accounts/teamname.html', {'form': form})


def restore_password(request, message=None):

    if request.method == 'POST':
        form = forms.RestorePasswordForm(request.POST)
        email = form['email'].value()
        # try:
        #     user = User.objects.get(email=email)
        # except:
        #     user = False
        #     message = 'YES'
            # return render(request, 'accounts/restore_password.html', {'form': form, 'message': message})
        try:
            user = User.objects.get(email=email)
            # print(user)
        except:
            user = False
            message = 'Пользователя с таким email нет'

        if form.is_valid() and user:
            password = password_generator()
            email = EmailMessage(
                'Новый пароль Fantasy Hockey',
                'Мы сделали вам новый пароль. \n'
                'Ваше имя пользователя: {}, \n'
                'пароль: {}.'.format(user.username, password),
                to=[user.email]
            )
            email.send()
            # print(password)  # !!!прислать письмо юзеру с новым паролем
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
    else:
        form = forms.RestorePasswordForm()

    return render(request, 'accounts/restore_password.html', {'form': form, 'message': message})


def conditions(request): # заставляет юзера заполнить название команды, если оно пусто
    if request.user.is_authenticated():
        current_user = request.user
        current_profile = Profile.objects.get(user_id=current_user)
        if current_profile.team_name:
            return redirect('play')
        else:
            return redirect('accounts:teamname')
    else:
        return redirect('accounts:login')


@login_required
def change_password(request):
   form = PasswordChangeForm(user=request.user, data=request.POST or None)
   if form.is_valid():
     form.save()
     update_session_auth_hash(request, form.user)
     return redirect('/')
   return render(request, 'accounts/change_password.html', {'form': form})