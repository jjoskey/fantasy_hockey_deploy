from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from players.models import Player
from accounts.models import Profile
from players.models import Team
# from players import views as players_views
# from players.views import *
import json
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


class LoggedinPage(TemplateView):
    template_name = 'loggedin.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    template_name = "index.html"


class PlayPage(TemplateView):

    template_name = "play.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['players'] = serializers.serialize('json', Player.objects.all())
    #     print(context['players'])
    #
    #     return context

def render_leaders(request):
    users = Profile.objects.filter(points__gt=0).order_by('-points')
    position = False
    # print(type(users))
    if request.user.is_authenticated(): # and current_profile in users:
        current_profile = Profile.objects.get(user_id=request.user)

        if current_profile in users:
            position = list(users).index(current_profile) + 1

    if len(users) > 100:
        users = users[:100]
    # print(type(users))
    print(position)

    return render(request, 'leaders.html', context={'users': users, 'position': position})


def render_user_team(request, user_id):
    profile = Profile.objects.get(pk=user_id)
    team = Team.objects.filter(user_id=profile, tour_number_end__isnull=True)
    team_dict = {'GK': [], 'DE': [], 'MF': [], 'FW': []}

    if len(team) == 11:
        for instance in team:
            team_dict[instance.player_id.position].append(instance)
        print(team_dict)
        print(profile.user_id.username)
        print(profile.points)
        return render(request, 'users_team.html', context={'team': team_dict, 'name': profile.user_id.username, 'points': profile.points})
    else:
        return HttpResponseNotFound(f'<h1>У такого пользователя нет команды, или что-то пошло не так...</h1>')