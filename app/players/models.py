from django.db import models
from accounts.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import validate_comma_separated_integer_list


class Tour(models.Model):
    season = models.PositiveIntegerField(blank=False, null=False, default=2019)
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=64, blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    supposed_end_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
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
    points = models.PositiveIntegerField(blank=False, null=False, default=0, editable=False)

    def __str__(self):
        return str(self.club) + ', ' + self.surname + ' ' + self.name


class Game(models.Model):

    tour_number = models.ForeignKey(Tour) #добавить сюда ссылка на Tour Model + добавить номер игры
    game_of_tour = models.PositiveSmallIntegerField(null=False, blank=False)
    home_team = models.ForeignKey(Club, related_name='Home')
    guest_team = models.ForeignKey(Club, related_name='Guest')
    score = models.CharField(validators=[validate_comma_separated_integer_list], max_length=5)
    bullitt_winner = models.ForeignKey(Club, related_name='Bullitt_Winner', null=True, blank=True)

    def __str__(self):
        return 'тур ' + str(self.tour_number) + ', игра: ' + str(self.game_of_tour) + ', ' + self.home_team.name + ' - ' + self.guest_team.name


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

    user_id = models.ForeignKey(Profile, editable=False)
    tour_number = models.ForeignKey(Tour, editable=False) #добавить сюда ссылка на Tour Model
    points = models.PositiveIntegerField(editable=False, default=0)

    class Meta:

        unique_together = ['user_id', 'tour_number']


class Result_Players(models.Model):

    player_id = models.ForeignKey(Player, editable=False)
    tour_number = models.ForeignKey(Tour, editable=False)
    points = models.PositiveIntegerField(editable=False, default=0)

    def __str__(self):
        return str(self.player_id) + ' ' + str(self.tour_number)

    class Meta:

        unique_together = ['player_id', 'tour_number']


class Miss_Match(models.Model):

    match_id = models.ForeignKey(Game)
    player_id = models.ForeignKey(Player)

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
