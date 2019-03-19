from django.db import models
from accounts.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import validate_comma_separated_integer_list
import datetime


YEAR = datetime.datetime.now().year


class Tour(models.Model):
    season = models.PositiveIntegerField(blank=False, null=False, default=YEAR,
                                         help_text='Год тура')
    number = models.PositiveSmallIntegerField(
        help_text='Номер тура. Если это матч плей-офф, номер всё равно вбивается. Он будет использован, при подсчёте очков.')
    name = models.CharField(max_length=64, blank=True, null=True,
                            help_text='Имя тура заполняется только во время плей-офф. Например, "1/8 финала"')
    start_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                      help_text='Начало дедлайна в туре.')
    supposed_end_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                             help_text='Предположительные время конца дедлайна в туре. Показывается для пользователя, когда ему ждать результатов подсчёта очков.')
    end_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return 'Сезон: ' + str(self.season) + ' тур: ' + str(self.number)

    class Meta:

        unique_together = ['season', 'number']




# @receiver(post_save, sender=Tour)
# def add_new_tour(sender, **kwargs):
#     obj = kwargs['instance']
#     if obj.end_time:
#         Tour.objects.create(number=obj.tour+1)


class Club(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Player(models.Model):

    club = models.ForeignKey(Club)
    surname = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)

    GOALKEEPER = 'GK'
    DEFENDER = 'DE'
    MIDFIELDER = 'MF'
    FORWARD = 'FW'

    POSITION_CHOICES = (
        (GOALKEEPER, 'GOALKEEPER'),
        (DEFENDER, 'DEFENDER'),
        (MIDFIELDER, 'MIDFIELDER'),
        (FORWARD, 'FORWARD')
    )

    position = models.CharField(max_length=2, choices=POSITION_CHOICES, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    points = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return str(self.club) + ', ' + self.surname + ' ' + self.name


class Game(models.Model):

    tour_number = models.ForeignKey(Tour, help_text='Тур, в который прошла игра')
    game_of_tour = models.PositiveSmallIntegerField(null=False, blank=False, help_text='Номер игры в туре (в туре может пройти больше двух игр)')
    home_team = models.ForeignKey(Club, related_name='Home', help_text='Команда, которая играла дома')
    guest_team = models.ForeignKey(Club, related_name='Guest', help_text='Команда, которая играла на выезде')
    score = models.CharField(validators=[validate_comma_separated_integer_list], max_length=5, null=True, blank=True,
                             help_text='Очки, записанные через запятую БЕЗ пробелов, например "2,1"')
    bullitt_winner = models.ForeignKey(Club, related_name='Bullitt_Winner', null=True, blank=True,
                                       help_text='Победитель по буллитам. Поле заполняется только когда матч закончен в ничью')
    start_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                      help_text='Время, когда игра начнётся. Время вписывается по часовому поясу UTC.')

    def __str__(self):
        return 'тур ' + str(self.tour_number) + ', игра: ' + str(self.game_of_tour) + ', ' + self.home_team.name + ' - ' + self.guest_team.name

    def split_score_in_template(self):
        return self.score.split(',')

    def winner(self):
        scores = list(map(int, self.score.split(',')))
        if scores[0] > scores[1]:
            return self.home_team
        elif scores[0] < scores[1]:
            return self.guest_team
        else:
            return self.bullitt_winner

    class Meta:
        unique_together = ['tour_number', 'game_of_tour', 'home_team', 'guest_team']


class Event(models.Model):

    match_id = models.ForeignKey(Game)

    GOAL_FROM_THE_GAME = 'Goal_Game'
    GOAL_FROM_THE_PENALTY = 'Goal_Penalty'
    GOAL_FROM_THE_FREE_KICK = 'Goal_Free_Kick'
    GREEN_CARD = 'Green_Card'
    YELLOW_CARD = 'Yellow_Card'
    RED_CARD = 'Red_Card'

    EVENT_CHOICES = (
        (GOAL_FROM_THE_GAME, 'GOAL_FROM_THE_GAME'),
        (GOAL_FROM_THE_PENALTY, 'GOAL_FROM_THE_PENALTY'),
        (GOAL_FROM_THE_FREE_KICK, 'GOAL_FROM_THE_FREE_KICK'),
        (GREEN_CARD, 'GREEN_CARD'),
        (YELLOW_CARD, 'YELLOW_CARD'),
        (RED_CARD, 'RED_CARD'),
    )

    kind = models.CharField(max_length=14, choices=EVENT_CHOICES, blank=False)
    player_id = models.ForeignKey(Player, blank=False, null=False)

    def __str__(self):
        return str(self.match_id) + ' ' + str(self.kind)


class Team(models.Model):

    user_id = models.ForeignKey(Profile)
    player_id = models.ForeignKey(Player)
    tour_number_start = models.ForeignKey(Tour, blank=True, null=True, related_name='tour_number_start') #добавить сюда ссылка на Tour Model + сделать автофилл
    tour_number_end = models.ForeignKey(Tour, blank=True, null=True, related_name='tour_number_end') #добавить сюда ссылка на Tour Model + сделать автофилл
    is_captain = models.BooleanField(blank=False, null=False, default=False)

    # def save(self, *args, **kwargs):
    #
    #     super(Team, self).save(*args, **kwargs) https://www.youtube.com/watch?v=pGVvG2b0oo8 если что посмотреть здесь,
    # как переделать метод self


    def __str__(self):
        return str(self.user_id) + ' ' + str(self.player_id) + ' ' + str(self.tour_number_start) + '-' + str(self.tour_number_end)

    def get_start_tour(self):
        return self.tour_number_start.number

    def get_end_tour(self):
        return self.tour_number_end.number

    class Meta:
        unique_together = ('user_id', 'player_id', 'tour_number_start')


class Team_Temporary(models.Model):

    user_id = models.ForeignKey(Profile)
    player_id = models.ForeignKey(Player)

    FIRST_TIME = 'First_Time'
    FROM_TEAM = 'From_Team'
    TO_TEAM = 'To_Team'

    TRANSFER_CHOICES = (
        (FIRST_TIME, 'FIRST_TIME'),
        (FROM_TEAM, 'FROM_TEAM'),
        (TO_TEAM, 'TO_TEAM'),
    )

    transfer = models.CharField(max_length=10, choices=TRANSFER_CHOICES, blank=False)
    timeout = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):

        return 'Temp' + str(self.user_id) + ' ' + str(self.player_id) + ' ' + str(self.timeout)


class Result_Profiles(models.Model):

    user_id = models.ForeignKey(Profile)
    tour_number = models.ForeignKey(Tour)
    points = models.IntegerField(default=0)

    class Meta:

        unique_together = ['user_id', 'tour_number']


class Result_Players(models.Model):

    player_id = models.ForeignKey(Player, editable=False)
    tour_number = models.ForeignKey(Tour, editable=False)
    points = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return str(self.player_id) + ' ' + str(self.tour_number)

    class Meta:

        unique_together = ['player_id', 'tour_number']


class Miss_Match(models.Model):

    match_id = models.ForeignKey(Game, help_text='Матч, который пропустил игрок')
    player_id = models.ForeignKey(Player, help_text='Игрок, пропустивший матч')

    def __str__(self):
        return str(self.match_id) + str(self.player_id)

    class Meta:

        unique_together = ['match_id', 'player_id']

class Captain(models.Model):

    user_id = models.ForeignKey(Profile)
    tour_number = models.ForeignKey(Tour)
    player_id = models.ForeignKey(Player)

    class Meta:

        unique_together = ['user_id', 'tour_number']


class Players_Team_in_Tour(models.Model):

    tour_number = models.ForeignKey(Tour, blank=False, null=False)
    player_id = models.ForeignKey(Player, blank=False, null=False)
    club = models.ForeignKey(Club, blank=False, null=False)

    class Meta:
        unique_together = ['player_id', 'tour_number', 'club']


class Off_Season(models.Model):

    start_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

