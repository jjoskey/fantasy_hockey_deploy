from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Club, Player, Game, Event, Team, Tour, Result_Players, Miss_Match, Result_Profiles, Team_Temporary, Captain
from django.core import serializers
from accounts.models import Profile, DEFAULT_BUDGET
from freeze_and_count import views as freeze_and_count
import datetime
from django.core.mail import EmailMessage


DEFAULT_CLUBS_Q = 3
DEFAULT_PLAYERS_Q = 11
DEFAULT_POS_Q = {'GK': [1, 'вратарь'], 'DE': [3, 'защитника'], 'MF': [4, 'полузащитника'], 'FW': [3, 'нападающих']}
YEAR = datetime.datetime.now().year
DELTA = datetime.timedelta(hours=1)


def get_users_temporary_team(user):
    utc_now, players = datetime.datetime.now(datetime.timezone.utc), []
    instances_from_team = Team.objects.filter(user_id__user_id=user).exclude(tour_number_end__isnull=False)
    instances_from_team_temp = Team_Temporary.objects.filter(user_id__user_id=user, timeout__gt=utc_now)

    for instance in instances_from_team:
        players.append(instance.player_id)

    for instance in instances_from_team_temp:
        if instance.transfer == 'From_Team':
            players.remove(instance.player_id)
        else:
            players.append(instance.player_id)

    return players


def permissions(players):

    clubs = Club.objects.all()

    data_to_return = {
        'clubs': {},
        'positions': {'GK': 0, 'DE': 0, 'MF': 0, 'FW': 0},
        'avaliable_budget': DEFAULT_BUDGET,
        'players_quantity': 0
    }

    for club in clubs:
        data_to_return['clubs'][club.name] = 0

    for player in players:
        data_to_return['clubs'][player.club.name] += 1
        data_to_return['positions'][player.position] += 1
        data_to_return['avaliable_budget'] -= player.price
        data_to_return['avaliable_budget'] = round(data_to_return['avaliable_budget'], 1)
        data_to_return['players_quantity'] += 1

    return data_to_return


def save_budget(user, budget):
    current_profile = Profile.objects.get(user_id=user)
    current_profile.budget = budget
    current_profile.save()


def all_players_to_send(temporary_team):
    players = Player.objects.all()
    all_player_data, permission_data = list(), permissions(temporary_team)

    for player in players:
        message = []
        disable = False

        if permission_data['players_quantity'] == DEFAULT_PLAYERS_Q:
            disable = True
            message.append('Ваша команда уже собрана.')

        else:

            if player in temporary_team:
                disable = True
                message.append('Этот игрок в вашей команде.')

            if permission_data['clubs'][player.club.name] >= DEFAULT_CLUBS_Q:
                disable = True
                message.append('В вашей команде уже {} игрока из клуба "{}".'.format(DEFAULT_CLUBS_Q, player.club.name))

            if permission_data['positions'][player.position] >= DEFAULT_POS_Q[player.position][0]:
                disable = True
                message.append('В вашей команде уже есть {} {}.'.format(DEFAULT_POS_Q[player.position][0], DEFAULT_POS_Q[player.position][1]))

            if permission_data['avaliable_budget'] < player.price:
                disable = True
                message.append('На этого игрока не хватает вашего бюджета.')

        all_player_data.append({
            'id': player.pk,
            'disable': disable,
            'message': message,
            'fields': {
                'club': player.club.name,
                'surname': player.surname,
                'name': player.name,
                'position': player.position,
                'price': player.price,
                'points': player.points
            }})
    return sorted(all_player_data, key=lambda x: (x['fields']['points'], x['fields']['price']), reverse=True)


def users_players_to_send(temporary_team, user):

    users_players_data, message = list(), ''
    is_first_time = freeze_and_count.is_first_time(user)
    is_freeze_now = freeze_and_count.is_freeze_now()
    current_profile = Profile.objects.get(user_id=user)
    message = []

    if is_freeze_now:

        if is_first_time:
            disable = False
        else:
            disable = True
            message.append('Дедлайн уже наступил')
    else:
        if is_first_time:
            disable = False
        else:
            if current_profile.changes_count:
                disable = False
            else:
                disable = True
                message.append('У вас нет замен')

    for player in temporary_team:
        users_players_data.append({
            'id': player.pk,
            'disable': disable,
            'message': message,
            'fields': {
                'club': player.club.name,
                'surname': player.surname,
                'name': player.name,
                'position': player.position,
                'price': player.price
            }
        })
    return users_players_data


def inf_for_save_button(temporary_team, user):
    team_in_team_model = Team.objects.filter(user_id__user_id=user).exclude(tour_number_end__isnull=False)
    save = 'disable'
    if not team_in_team_model:
        if len(temporary_team) == DEFAULT_PLAYERS_Q:
            save = 'enable'

    else:
        if len(temporary_team) == DEFAULT_PLAYERS_Q:
            for instance in team_in_team_model:
                if instance.player_id in temporary_team:
                    continue
                else:
                    save = 'enable'
    return save


def inf_for_cancel_button(user):
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    if Team_Temporary.objects.filter(user_id__user_id=user, transfer='From_Team', timeout__gt=utc_now):
        return 'enable'
    else:
        return 'disable'


def captain_stage(user):
    current_profile = Profile.objects.get(user_id=user)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    users_team = Team.objects.filter(user_id=current_profile).exclude(tour_number_end__isnull=False)
    is_captain = users_team.filter(user_id=current_profile, is_captain=True).exclude(tour_number_end__isnull=False).exists()
    team_temp = Team_Temporary.objects.filter(user_id=current_profile, timeout__gt=utc_now).exists()

    if freeze_and_count.is_freeze_now():
        if freeze_and_count.is_first_time(user):
            return 'wait_for_team'
        else:
            if is_captain:
                return 'freeze'
            else:
                next_tour = freeze_and_count.get_next_tour()

                for instance in users_team:
                    if instance.tour_number_start != next_tour:
                        return 'freeze'
                return 'choose_captain'

    else:
        if freeze_and_count.is_first_time(user):
            return 'wait_for_team'
        else:
            if team_temp:
                return 'wait_for_team'
            if is_captain:
                return 'can_choose_another'
            else:
                return 'choose_captain'


def get_results_of_3_last_tours(user):
    dict_to_return = dict()
    profile = Profile.objects.get(user_id=user)
    last_3_tours_result = Result_Profiles.objects.filter(tour_number__season=YEAR, user_id=profile).order_by('-id')[:3]
    for instance in last_3_tours_result:
        dict_to_return[instance.tour_number.number] = instance.points
    return dict_to_return


def collect_data(user):
    temporary_team = get_users_temporary_team(user)
    all_players = all_players_to_send(temporary_team)
    users_players = users_players_to_send(temporary_team, user)
    budget = permissions(temporary_team)['avaliable_budget']
    save = inf_for_save_button(temporary_team, user)
    cancel = inf_for_cancel_button(user)
    captain_stage_user = captain_stage(user)
    last_3_tours_result = get_results_of_3_last_tours(user)
    current_profile = Profile.objects.get(user_id=user)
    changes = current_profile.changes_count
    if Team.objects.filter(user_id=current_profile, is_captain=True).exclude(
        tour_number_end__isnull=False).exists():
        captain = Team.objects.get(user_id__user_id=user, is_captain=True, tour_number_end__isnull=True)
    else: captain = False

    tour_info = get_tour_info_for_front()

    return {
        'all_players': all_players,
        'users_players': users_players,
        'budget': budget,
        'save': save,
        'cancel': cancel,
        'changes': changes,
        'captain_stage': captain_stage_user,
        'captain': captain if captain == False else captain.player_id.pk,
        'tour_info': tour_info,
        'last_3_result': last_3_tours_result

    }


@csrf_exempt
def send_players_list(request): #фукнция, которая вызывается при отрисовке на странице play.html

    if request.method == 'GET':  #safety
        data_to_send = collect_data(request.user)

        return JsonResponse(data_to_send, safe=False)


def can_add_player_to_team(permission_data, player):
    can_add = True
    if permission_data['players_quantity'] == DEFAULT_PLAYERS_Q:
        can_add = False

    else:

        if permission_data['clubs'][player.club.name] >= DEFAULT_CLUBS_Q:
            can_add = False

        if permission_data['positions'][player.position] >= DEFAULT_POS_Q[player.position][0]:
            can_add = False

        if permission_data['avaliable_budget'] < player.price:
            can_add = False
    return can_add


def add_player_to_team_temporary(player, user):

    utc_now = datetime.datetime.now(datetime.timezone.utc)
    permission_data = permissions(get_users_temporary_team(user))
    can_add = can_add_player_to_team(permission_data, player)
    current_profile = Profile.objects.get(user_id=user)

    if not Team_Temporary.objects.filter(
            user_id=current_profile,
            player_id=player,
            timeout__gt=utc_now).exists() and not Team.objects.filter(
            user_id__user_id=user, player_id=player).exclude(
            tour_number_end__isnull=False) and can_add:

        if freeze_and_count.is_first_time(user):

            Team_Temporary(user_id=current_profile, player_id=player, transfer='First_Time',
                           timeout=utc_now+DELTA if not get_time_of_first_player_in_temp_team(user) else get_time_of_first_player_in_temp_team(user)).save()

        else:

            Team_Temporary(user_id=current_profile, player_id=player, transfer='To_Team',
                           timeout=utc_now+DELTA if not get_time_of_first_player_in_temp_team(user) else get_time_of_first_player_in_temp_team(user)).save()
            transform_change_count(current_profile, -1)

    else:
        instance = Team_Temporary.objects.get(user_id=current_profile, player_id=player, timeout__gt=utc_now)
        instance.timeout = utc_now
        instance.save()


def transform_change_count(profile, delta):
    profile.changes_count += delta
    profile.save()


@csrf_exempt
def receive_player_id_to_add(request):  #safety
    if request.method == 'POST':
        player_id = json.loads(request.body)
        # print(player_id)
        player = Player.objects.get(pk=player_id)

        add_player_to_team_temporary(player, request.user)

        return HttpResponse('OK')


@csrf_exempt
def receive_player_id_to_unactivate(request):  #safety
    if request.method == 'POST':

        player = Player.objects.get(pk=json.loads(request.body))

        unactivate_player_in_temporary_team_if_received(player, request.user)

        return HttpResponse('OK')


@csrf_exempt
def receive_captains_id(request):  #safety
    player = Player.objects.get(pk=json.loads(request.body))
    make_player_captain(player, request.user)
    return HttpResponse('OK')


def unactivate_player_in_temporary_team_if_received(player, user):

    utc_now = datetime.datetime.now(datetime.timezone.utc)
    current_profile = Profile.objects.get(user_id=user)

    if freeze_and_count.is_first_time(user):

        instance = Team_Temporary.objects.get(user_id=current_profile, player_id=player, transfer='First_Time',
                       timeout__gt=utc_now)
        instance.timeout = utc_now
        instance.save()

    else:
        if Team_Temporary.objects.filter(user_id=current_profile, player_id=player, transfer='To_Team', timeout__gt=utc_now).exists():
            instance = Team_Temporary.objects.get(user_id=current_profile, player_id=player, transfer='To_Team',
                       timeout__gt=utc_now)
            instance.timeout = utc_now
            instance.save()
            current_profile.changes_count += 1
            current_profile.save()
        else:

            if Team_Temporary.objects.filter(user_id=current_profile, player_id=player, transfer='From_Team',
                              timeout__gt=utc_now).exists():
                return
            Team_Temporary(user_id=current_profile, player_id=player, transfer='From_Team',
                       timeout=utc_now+DELTA if not get_time_of_first_player_in_temp_team(user) else get_time_of_first_player_in_temp_team(user)).save()


@csrf_exempt
def save_team(request):  #safety
    if request.method == 'POST':
        save_users_in_team_model(request.user)
        return HttpResponse('OK')



@csrf_exempt
def cancel_transfers(request):
    if request.method == 'POST':  #safety
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        instances_in_temp_team = Team_Temporary.objects.filter(user_id__user_id=request.user, timeout__gt=utc_now)
        current_profile = Profile.objects.get(user_id=request.user)
        for instance in instances_in_temp_team:
            if instance.transfer == 'To_Team':
                transform_change_count(current_profile, 1)
            instance.timeout = utc_now
            instance.save()
        return HttpResponse('OK')


def save_users_in_team_model(user):

    current_profile = Profile.objects.get(user_id=user)
    temporary_team = get_users_temporary_team(user)
    current_tour = freeze_and_count.get_current_tour()
    next_tour = freeze_and_count.get_next_tour()
    previous_tour = freeze_and_count.get_previous_tour()
    first_time = freeze_and_count.is_first_time(user)
    freeze_now = freeze_and_count.is_freeze_now()
    budget = permissions(temporary_team)['avaliable_budget']
    current_profile.budget = budget
    current_profile.save()

    if first_time:

        if freeze_now:

            for player in temporary_team:
                Team(user_id=current_profile, player_id=player, tour_number_start=next_tour).save()
                unactivate_player_in_temporary_team_if_saved(player, user)

        else:

            for player in temporary_team:
                Team(user_id=current_profile, player_id=player, tour_number_start=current_tour).save()
                unactivate_player_in_temporary_team_if_saved(player, user)

    else:

        if not freeze_now:
            instances_from_team = Team.objects.filter(user_id__user_id=user).exclude(tour_number_end__isnull=False)

            for instance in instances_from_team:
                if instance.player_id in temporary_team:
                    temporary_team.remove(instance.player_id)
                else:
                    if previous_tour == 'Previous tour is not exist':
                        instance.delete()
                        unactivate_player_in_temporary_team_if_saved(instance.player_id, user)
                    else:
                        instance.tour_number_end = previous_tour
                        instance.save()
                        unactivate_player_in_temporary_team_if_saved(instance.player_id, user)
                        if instance.get_end_tour() < instance.get_start_tour():
                            instance.delete()

            for player in temporary_team:
                Team(user_id=current_profile, player_id=player, tour_number_start=current_tour).save()
                unactivate_player_in_temporary_team_if_saved(player, user)


def unactivate_player_in_temporary_team_if_saved(player, user):
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    current_profile = Profile.objects.get(user_id=user)
    player_in_temp = Team_Temporary.objects.get(
        user_id=current_profile,
        player_id=player,
        timeout__gt=utc_now
    )
    player_in_temp.timeout = utc_now
    player_in_temp.save()


def get_time_of_first_player_in_temp_team(user):
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    current_profile = Profile.objects.get(user_id=user)

    instance = Team_Temporary.objects.filter(user_id=current_profile, timeout__gt=utc_now).first()
    if instance is None:
        return None
    else:
        return instance.timeout


def make_player_captain(player, user):
    current_profile = Profile.objects.get(user_id=user)
    users_team = Team.objects.filter(user_id=current_profile).exclude(tour_number_end__isnull=False)

    for instance in users_team:
        if instance.is_captain:
            instance.is_captain = False
            instance.save()

    next_captain = Team.objects.get(user_id=current_profile, player_id=player, tour_number_end__isnull=True)
    next_captain.is_captain = True
    next_captain.save()


def get_tour_info_for_front():
    current_tour = freeze_and_count.get_current_tour()
    if freeze_and_count.is_freeze_now():
        if not current_tour.name:
            return {'tour': current_tour.number, 'deadline_end': current_tour.supposed_end_time}
        else:
            return {'tour_name': current_tour.name, 'deadline_end': current_tour.supposed_end_time}
    else:
        if not current_tour.name:
            return {'tour': current_tour.number, 'deadline': current_tour.start_time}
        else:
            return {'tour_name': current_tour.name, 'deadline': current_tour.start_time}
