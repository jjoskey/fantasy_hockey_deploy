from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import datetime
import json
from django.utils import dateparse
from players.models import Club, Player, Game, Event, Team, Tour, Result_Players, Miss_Match, Result_Profiles, Team_Temporary, Captain, Players_Team_in_Tour, Off_Season
from accounts.models import Profile
from players.views import DEFAULT_PLAYERS_Q
from django.db.models import Q
from players import views


YEAR = datetime.datetime.now().year
DEFAULT_CHANGES_COUNT = 3


@staff_member_required
def render_freeze_and_count(request):
    # tour = get_current_tour()
    # save_players_in_PTT_model(tour)
    return render(request, 'freeze_and_count.html')


def get_current_tour():

    tours = Tour.objects.all()
    current_tour = None

    if tours:

        for tour in tours:
            if tour.end_time:
                continue
            else:
                current_tour = tour
                break

        if current_tour is None:

            current_tour = Tour.objects.create(number=1, season=tours[len(tours)-1].season + 1)

    else:

        current_tour = Tour.objects.create(number=1, season=2019)

    return current_tour


def get_next_tour():
    current_tour = get_current_tour()
    current_number, current_season = current_tour.number, current_tour.season
    try:
        next_tour = Tour.objects.get(number=current_number+1, season=current_season)
        return next_tour
    except Exception:
        return 'Next tour is in the next season'


def get_previous_tour():
    current_tour = get_current_tour()
    current_number, current_season = current_tour.number, current_tour.season
    if current_number == 1:
        return 'Previous tour is not exist'
    else:
        previous_tour = Tour.objects.get(number=current_number-1, season=current_season)
        return previous_tour


def get_freeze_data():

    current_tour = get_current_tour()
    data_to_send = dict()
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    if not current_tour.start_time:
        data_to_send['message'] = 'Danger!'
        data_to_send['time'] = ''
    else:
        if current_tour.start_time < utc_now:
            data_to_send['message'] = "It's freeze time"
            data_to_send['time'] = current_tour.start_time
        else:
            data_to_send['message'] = 'Freeze time is coming soon'
            data_to_send['time'] = current_tour.start_time
    data_to_send['tour'] = current_tour.number

    return data_to_send


@csrf_exempt
def send_last_freeze(request): #запускается, когда пользователь заходит на /freeze_and_count/

    # players = Player.objects.all()
    # for player in players:
    #
    #     player.price = player.price / 1000000
    #     player.save()


    if request.method == 'GET':
        data_to_send = get_freeze_data()
        print(data_to_send)
        return JsonResponse(data_to_send, safe=False)


@csrf_exempt
def off_season(request):
    pass


@csrf_exempt
def start_season(request):
    pass


@csrf_exempt
def receive_freeze_data(request):

    if request.method == 'POST':
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        freeze_data = json.loads(request.body)
        current_tour = get_current_tour()

        if freeze_data['message'] == 'Finish freeze time':
            current_tour.end_time = utc_now
            current_tour.save()
        elif freeze_data['message'] == 'Start freeze time':
            current_tour.start_time = utc_now
            current_tour.save()

        return HttpResponse('OK')


def get_or_create_key_and_plus_value(dct: dict, player_id, points, message):
    dct.setdefault(player_id, {'points': 0, 'purposes': [], 'player_name': ''})
    dct[player_id]['points'] += points
    dct[player_id]['purposes'].append(message)
    if not dct[player_id]['player_name']:
        dct[player_id]['player_name'] = str(Player.objects.get(pk=player_id))


def miss_the_match(player, miss_match_instances):

    if miss_match_instances.exists():
        for instance in miss_match_instances:
            if instance.player_id == player:
                return True
    return False


def profile_can_play(profile):
    current_tour = get_current_tour()
    if len(Team.objects.filter(user_id=profile,
                               tour_number_start__season=YEAR,
                               tour_number_start__number__lte=current_tour.number, tour_number_end__isnull=True)) == DEFAULT_PLAYERS_Q:
        return True
    return False


def save_players_in_PTT_model(tour):
    players = Player.objects.all()
    for player in players:
        Players_Team_in_Tour.objects.update_or_create(player_id=player, tour_number=tour, club=player.club)


def count_points(tour):

    current_tour = Tour.objects.get(number=tour, season=YEAR)
    events = Event.objects.filter(match_id__tour_number=current_tour)
    points = dict()
    instances_PTT = Players_Team_in_Tour.objects.filter(tour_number=current_tour)
    matches = Game.objects.filter(tour_number=current_tour)
    miss_match_instances = Miss_Match.objects.filter(match_id__tour_number=current_tour)


    for event in events:
        # if event.player_id.pk == 37:
        #     print(event.player_id.club)
        if event.kind == 'Goal_Game':

            if event.player_id.position == 'GK':
                get_or_create_key_and_plus_value(points, event.player_id.pk, 10, '+10, goal by GK')
            elif event.player_id.position == 'DE':
                get_or_create_key_and_plus_value(points, event.player_id.pk, 6, '+6, goal by FW')
            elif event.player_id.position == 'MF':
                get_or_create_key_and_plus_value(points, event.player_id.pk, 5, '+5, goal by MF')
            elif event.player_id.position == 'FW':
                get_or_create_key_and_plus_value(points, event.player_id.pk, 4, '+4, goal by FW')

        elif event.kind == 'Goal_Free_Kick':
            get_or_create_key_and_plus_value(points, event.player_id.pk, 3, '+3, goal FK')

        elif event.kind == 'Goal_Penalty':
            get_or_create_key_and_plus_value(points, event.player_id.pk, 2, '+2 goal PN')

        elif event.kind == 'Green_Card':
            get_or_create_key_and_plus_value(points, event.player_id.pk, -1, '-1, GC')

        elif event.kind == 'Yellow_Card':
            get_or_create_key_and_plus_value(points, event.player_id.pk, -3, '-3, YC')

        elif event.kind == 'Red_Card':
            get_or_create_key_and_plus_value(points, event.player_id.pk, -5, '-5, RC')

    for match in matches:

        score = list(map(int, match.score.split(',')))
        winner, loser, bullitt_winner = None, None, None
        if score[0] > score[1]:
            winner = match.home_team
            loser = match.guest_team
        elif score[0] < score[1]:
            winner = match.guest_team
            loser = match.home_team
        else: bullitt_winner = match.bullitt_winner

        for instance in instances_PTT.filter(Q(club=match.home_team) | Q(club=match.guest_team)):
            # if player.pk == 37:
            #     print(player)
            goals_scored_by_players_team = score[0] if instance.club == match.home_team else score[1]
            goals_miss_by_players_team = score[1] if instance.club == match.home_team else score[0]

            if not miss_the_match(instance.player_id, miss_match_instances.filter(match_id=match)):

                if instance.club == winner:
                    get_or_create_key_and_plus_value(points, instance.player_id.pk, 3, '+3, team won')
                elif instance.club == loser:
                    get_or_create_key_and_plus_value(points, instance.player_id.pk, -1, '-1, team lose')

                if winner == None:
                    get_or_create_key_and_plus_value(points, instance.player_id.pk, 1, '+1, draw')
                    if instance.club == bullitt_winner:
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, 1, '+1, bullitts won')

                if goals_miss_by_players_team >= 3:
                    if instance.player_id.position == 'GK':
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, -3, '-3, team miss 3+ goals GK')
                    elif instance.player_id.position == 'DE':
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, -2, '-2, team miss 3+ goals DE')

                if goals_scored_by_players_team >= 5:
                    if instance.player_id.position == 'MF':
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, 2, '+2, team scored 5+ goals MF')
                    elif instance.player_id.position == 'FW':
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, 3, '+3, team scored 5+ goals FW')

                if instance.club == winner and goals_miss_by_players_team == 0:
                    if instance.player_id.position == 'GK':
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, 5, '+5, team won and miss 0 goals GK')
                    elif instance.player_id.position == 'DE':
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, 3, '+3, team won and miss 0 goals DE')

                if goals_scored_by_players_team == 0 and goals_miss_by_players_team == 0:
                    if instance.player_id.position == 'GK' or instance.player_id.position == 'DE':
                        get_or_create_key_and_plus_value(points, instance.player_id.pk, 1, '+1, 0:0 draw GK or DE')

            else:
                get_or_create_key_and_plus_value(points, instance.player_id.pk, 0, '0, Miss {}'.format(match))

        # for player in players.filter(Q(club=match.home_team) | Q(club=match.guest_team)):
        #     # if player.pk == 37:
        #     #     print(player)
        #     goals_scored_by_players_team = score[0] if player.club == match.home_team else score[1]
        #     goals_miss_by_players_team = score[1] if player.club == match.home_team else score[0]
        #
        #     if not miss_the_match(player, miss_match_instances.filter(match_id=match)):
        #
        #         if player.club == winner:
        #             get_or_create_key_and_plus_value(points, player.pk, 3, '+3, team won')
        #         elif player.club == loser:
        #             get_or_create_key_and_plus_value(points, player.pk, -1, '-1, team lose')
        #
        #         if winner == None:
        #             get_or_create_key_and_plus_value(points, player.pk, 1, '+1, draw')
        #             if player.club == bullitt_winner:
        #                 get_or_create_key_and_plus_value(points, player.pk, 1, '+1, bullitts won')
        #
        #         if goals_miss_by_players_team >= 3:
        #             if player.position == 'GK':
        #                 get_or_create_key_and_plus_value(points, player.pk, -3, '-3, team miss 3+ goals GK')
        #             elif player.position == 'DE':
        #                 get_or_create_key_and_plus_value(points, player.pk, -2, '-2, team miss 3+ goals DE')
        #
        #         if goals_scored_by_players_team >= 5:
        #             if player.position == 'MF':
        #                 get_or_create_key_and_plus_value(points, player.pk, 2, '+2, team scored 5+ goals MF')
        #             elif player.position == 'FW':
        #                 get_or_create_key_and_plus_value(points, player.pk, 3, '+3, team scored 5+ goals FW')
        #
        #         if player.club == winner and goals_miss_by_players_team == 0:
        #             if player.position == 'GK':
        #                 get_or_create_key_and_plus_value(points, player.pk, 5, '+5, team won and miss 0 goals GK')
        #             elif player.position == 'DE':
        #                 get_or_create_key_and_plus_value(points, player.pk, 3, '+3, team won and miss 0 goals DE')
        #
        #         if goals_scored_by_players_team == 0 and goals_miss_by_players_team == 0:
        #             if player.position == 'GK' or player.position == 'DE':
        #                 get_or_create_key_and_plus_value(points, player.pk, 1, '+1, 0:0 draw GK or DE')
        #
        #     else:
        #         get_or_create_key_and_plus_value(points, player.pk, 0, '0, Miss {}'.format(match))

    return points


def save_players_results(tour, points):

    current_tour = Tour.objects.get(number=tour, season=YEAR)

    for key, value in points.items():
        current_player = Player.objects.get(pk=key)
        Result_Players.objects.update_or_create(player_id=current_player, tour_number=current_tour, defaults={'points': value['points']})


def save_captains_to_Captain_model(tour):
    profiles = Profile.objects.all()
    for profile in profiles:
        try:
            player = Team.objects.get(user_id=profile, tour_number_end__isnull=True, tour_number_start__number__lte=tour.number, is_captain=True).player_id
            # print(player)
        except:
            # print(profile)
            continue
        Captain.objects.update_or_create(user_id=profile, tour_number=tour, defaults={'player_id': player})


def save_profiles_results(tour, points):

    profiles = Profile.objects.all()
    tour_to_count = Tour.objects.get(number=tour, season=YEAR)
    if tour_to_count == get_current_tour():
        save_captains_to_Captain_model(tour)
    captains = Captain.objects.filter(tour_number=tour_to_count)

    for profile in profiles:

        if profile_can_play(profile):
            try:
                captain = captains.get(user_id=profile)
            except:
                captain = None

            result = 0

            for instance in Team.objects.filter(user_id=profile).filter(tour_number_start__number__lte=tour_to_count.number)\
                    .filter(Q(tour_number_end__isnull=True) | Q(tour_number_end__number__gte=tour_to_count.number)): #добавить фильтр по году
                try:
                    result_player = Result_Players.objects.get(player_id=instance.player_id, tour_number=tour_to_count).points
                except:
                    result_player = 0
                if captain is not None:
                    if instance.player_id == captain.player_id:
                        result += result_player * 2
                    else:
                        result += result_player
                else:
                    result += result_player

            Result_Profiles.objects.update_or_create(user_id=profile, tour_number=tour_to_count, defaults={'points':result})
        # else:
        #     recount_start_tour(profile)


def save_point_in_profile_model():

    for profile in Profile.objects.all():
        result = 0
        for instance in Result_Profiles.objects.filter(user_id=profile, tour_number__season=YEAR):
            result += instance.points
        profile.points = result
        profile.save()


def save_point_in_players_model():
    for player in Player.objects.all():
        result = 0
        for instance in Result_Players.objects.filter(player_id=player, tour_number__season=YEAR):
            result += instance.points
        player.points = result
        player.save()


@csrf_exempt
def count_and_save_points(request):

    if request.method == 'POST':
        tour = json.loads(request.body)
        tour_to_count = Tour.objects.get(number=tour, season=YEAR)
        if tour_to_count == get_current_tour():
            if is_freeze_now():
                save_players_in_PTT_model(tour_to_count)
                points = count_points(tour)

                save_players_results(tour, points)
                save_profiles_results(tour, points)
                save_point_in_profile_model()
                save_point_in_players_model()
                turn_changes_count_for_all_profiles_to_default()

                return JsonResponse(points, safe=False)
            else:
                return JsonResponse('Подсчёт очков можно делать только во freeze time.', safe=False)
        else:
            points = count_points(tour)

            save_players_results(tour, points)
            save_profiles_results(tour, points)
            save_point_in_profile_model()
            save_point_in_players_model()

            return JsonResponse(points, safe=False)


@csrf_exempt
def add_changes_using_data(request):

    if request.method == 'POST':
        changes = json.loads(request.body)
        add_changes_count_for_all_profiles(changes)

        return HttpResponse('OK')


def turn_changes_count_for_all_profiles_to_default(changes=DEFAULT_CHANGES_COUNT):
    profiles = Profile.objects.all()
    for profile in profiles:
        if is_first_time(profile.user_id):
            continue
        else:
            profile.changes_count = changes
            profile.save()


def add_changes_count_for_all_profiles(changes):
    profiles = Profile.objects.all()
    for profile in profiles:
        if is_first_time(profile.user_id):
            continue
        else:
            profile.changes_count += changes
            profile.save()


def is_freeze_now():
    freeze_data = get_freeze_data()
    if freeze_data['message'] == "It's freeze time":
        return True
    return False


def is_first_time(user):

    if Result_Profiles.objects.filter(user_id__user_id=user, tour_number__season=YEAR):
        return False
    else:
        current_tour = get_current_tour()
        users_team = Team.objects.filter(user_id__user_id=user,
                                         tour_number_start__season=YEAR,
                                         # tour_number_start__number__lte=current_tour.number,
                                         tour_number_end__isnull=True)

        if len(users_team) == DEFAULT_PLAYERS_Q:
            return False
        else:
            return True



# def recount_start_tour(profile):
#     next_tour = get_next_tour()
#     if is_first_time(profile.user_id):
#         for instance in Team.objects.filter(user_id=profile, tour_number_start__season=YEAR):
#             instance.tour_number_start = next_tour
#             instance.save()
