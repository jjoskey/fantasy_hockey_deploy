from django.contrib import admin
from .models import Club, Player, Game, Event, Team, Tour, Result_Players, Miss_Match, Result_Profiles, Team_Temporary, Captain, Players_Team_in_Tour, Off_Season
from django.contrib.auth.models import Group, User
from django.db.models import Q


class ClubAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']


class PlayerAdmin(admin.ModelAdmin):

    list_display = ['id', 'club', 'surname', 'name', 'position', 'price', 'points']
    list_filter = ['club', 'position']


class EventInline(admin.TabularInline):
    model = Event
    extra = 0


class MissMatchInline(admin.TabularInline):
    model = Miss_Match
    extra = 0


class GameAdmin(admin.ModelAdmin):

    list_display = ['tour_number', 'game_of_tour', 'home_team', 'guest_team', 'score', 'bullitt_winner', 'start_time']
    inlines = [EventInline, MissMatchInline]
    list_filter = ['tour_number', 'home_team', 'guest_team']


class EventAdmin(admin.ModelAdmin):

    list_display = ['id', 'match_id', 'kind', 'player_id']
    list_filter = ['match_id__tour_number', 'player_id__club']


class TeamAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'player_id', 'tour_number_start', 'tour_number_end', 'is_captain']


class TourAdmin(admin.ModelAdmin):

    list_display = ['number', 'name', 'start_time', 'supposed_end_time', 'end_time', 'season']
    search_fields = ['user_id']


class ResultProfilesAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'tour_number', 'points']


class ResultPlayersAdmin(admin.ModelAdmin):

    list_display = ['player_id', 'tour_number', 'points']


class MissMatchAdmin(admin.ModelAdmin):

    list_display = ['match_id', 'player_id']
    list_filter = ['match_id__tour_number']


class TeamTemporaryAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'player_id', 'transfer', 'timeout']
    search_fields = ['user_id']


class CaptainAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'tour_number', 'player_id' ]
    list_filter = ['user_id', 'tour_number']
    search_fields = ['user_id']


class PTTAdmin(admin.ModelAdmin):

    list_display = ['tour_number', 'player_id', 'club']


class OffSeasonAdmin(admin.ModelAdmin):

    list_display = ['start_time', 'end_time']


admin.site.register(Club, ClubAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Result_Profiles, ResultProfilesAdmin)
admin.site.register(Miss_Match, MissMatchAdmin)
admin.site.register(Result_Players, ResultPlayersAdmin)
admin.site.register(Team_Temporary, TeamTemporaryAdmin)
admin.site.register(Captain, CaptainAdmin)
admin.site.register(Players_Team_in_Tour, PTTAdmin)
admin.site.register(Off_Season, OffSeasonAdmin)


admin.site.unregister(Group)
# admin.site.unregister(User)
admin.site.site_header = 'Russian Fantasy Hockey'
