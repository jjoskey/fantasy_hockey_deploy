from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from . import forms
from django.http import HttpResponseRedirect
from .models import Profile


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
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