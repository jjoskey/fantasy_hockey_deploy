from django.views.generic import TemplateView
from accounts.models import Profile, AdBanners
from players.models import Team, Game
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from freeze_and_count import views as freeze_and_count
from players import views as players
from django.contrib.auth.models import User
import datetime


class LoggedinPage(TemplateView):
    template_name = 'loggedin.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


def render_rules(request):
    utc_now = datetime.datetime.now(datetime.timezone.utc)

    try:
        banners = AdBanners.objects.get(start_time__lte=utc_now, end_time__gte=utc_now)
    except:
        banners = False

    return render(request, 'rules.html', context={'banners': banners})


def render_play_page(request):

    if request.user.is_authenticated():
        last_3_results = players.get_results_of_3_last_tours(request.user)
        off_season = freeze_and_count.is_off_season()
        current_profile = Profile.objects.get(user_id=request.user)
        if current_profile.team_name:
            utc_now = datetime.datetime.now(datetime.timezone.utc)
            try:
                banners = AdBanners.objects.get(start_time__lte=utc_now, end_time__gte=utc_now)
            except:
                banners = False

            return render(request, 'play.html', context={'banners': banners, 'off_season': off_season, 'results': last_3_results})
        else:
            return redirect('accounts:teamname')
    else:
        return redirect('accounts:login')


def render_leaders(request):
    off_season = freeze_and_count.is_off_season()
    users = Profile.objects.filter(points__gt=0).order_by('-points')
    position = False
    points = False
    # print(type(users))
    if request.user.is_authenticated(): # and current_profile in users:
        current_profile = Profile.objects.get(user_id=request.user)

        if current_profile in users:
            position = list(users).index(current_profile) + 1
            points = current_profile.points

    if len(users) > 100:
        users = users[:100]

    utc_now = datetime.datetime.now(datetime.timezone.utc)
    try:
        banners = AdBanners.objects.get(start_time__lte=utc_now, end_time__gte=utc_now)
    except:
        banners = False

    return render(request, 'leaders.html', context={'users': users, 'position': position, 'points': points, 'banners': banners, 'off_season': off_season})


def choose_tshirt(player_id):
    if player_id.club.name == 'Динамо-Строитель':
        return 'images/play/1_shirt_DS.png'
    elif player_id.club.name == 'Динамо-Электросталь':
        return 'images/play/2_shirt_DE.png'
    elif player_id.club.name == 'Динамо-Казань':
        return 'images/play/3_shirt_DK.png'
    elif player_id.club.name == 'Динамо-ЦОП':
        return 'images/play/4_shirt_DCOP.png'
    elif player_id.club.name == 'Тана':
        return 'images/play/6_shirt_TANA.png'
    elif player_id.club.name == 'СПБ УОР2':
        return 'images/play/5_shirt_SPB.png'
    elif player_id.club.name == 'Волна':
        return 'images/play/7_shirt_VOLNA.png'


def render_user_team(request, user_id):

    profile = Profile.objects.get(pk=user_id)
    user = User.objects.get(pk=user_id)
    team_instances = Team.objects.filter(user_id=profile, tour_number_end__isnull=True)
    team = {'GK': [], 'DE': [], 'MF': [], 'FW': []}
    last_3_results = players.get_results_of_3_last_tours(user)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    captain = False
    try:
        banners = AdBanners.objects.get(start_time__lte=utc_now, end_time__gte=utc_now)
    except:
        banners = False

    if len(team_instances) == 11:  # поставить вместо 11 - players.DEFAULT_PLAYERS_Q
        for instance in team_instances:
            instance.player_id.tshirt = choose_tshirt(instance.player_id)
            team[instance.player_id.position].append(instance.player_id)
            if instance.is_captain:
                captain = instance.player_id

        return render(request, 'users_team.html', context={'team': team, 'name': profile.team_name, 'points': profile.points, 'results': last_3_results, 'banners': banners, 'captain': captain})
    else:
        return HttpResponseNotFound(f'<h1>У такого пользователя нет команды, или что-то пошло не так...</h1>')


def render_home_page(request):

    current_tour = freeze_and_count.get_current_tour()
    previous_tour = freeze_and_count.get_previous_tour()
    ct_games = Game.objects.filter(tour_number=current_tour)
    pt_games = False

    if not ct_games:
        ct_games = False

    if previous_tour == 'Previous tour is not exist':
        previous_tour = False

    if previous_tour:
        pt_games = Game.objects.filter(tour_number=previous_tour)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    try:
        banners = AdBanners.objects.get(start_time__lte=utc_now, end_time__gte=utc_now)
    except:
        banners = False
    print(banners)
    return render(request, 'index.html', context={'ct_games': ct_games, 'pt_games': pt_games, 'current_tour': current_tour, 'previous_tour': previous_tour, 'banners': banners})
