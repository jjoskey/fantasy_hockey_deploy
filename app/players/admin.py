from django.contrib import admin
from .models import Club, Player, Game, Event, Team, Tour, Result_Players, Miss_Match, Result_Profiles, Team_Temporary, Captain
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

class EventAdmin(admin.ModelAdmin):

    list_display = ['id', 'match_id', 'kind', 'player_id']

#     fields = ['match_id', 'kind', 'player_id']
#     readonly_fields = ['match_id']
#
#     initial_fields = ['match_id', 'kind']
#     initial_readonly_fields = []
#     selected_match = None
#
#     # # standard attributes (used in "change" view)
#     # fields = ['country', 'city']
#     # readonly_fields = ['country']
#     #
#     # # custom attributes (used in "add" view)
#     # initial_fields = ['country']
#     # initial_readonly_fields = []
#     # selected_country = None
#
#     def get_fields(self, request, obj=None):
#         """ show initial fields in add view, show all fields in change view """
#         fields = super().get_fields(request, obj)
#         if obj is None:
#             fields = self.initial_fields
#         return fields
#
#     def get_readonly_fields(self, request, obj=None):
#         """ set the initial field readonly in the change view """
#         readonly_fields = super().get_readonly_fields(request, obj)
#         if obj is None:
#             readonly_fields = self.initial_readonly_fields
#         return readonly_fields
#
#     def add_view(self, request, form_url='', extra_context=None):
#         """ remove the save button from the "add" view """
#         extra_context = dict(show_save=False, show_save_and_add_another=False, really_hide_save_and_add_another_damnit=True)
#         # extra_context['show_save_and_add_another'] = False
#         # extra_context['really_hide_save_and_add_another_damnit'] = True
#         return super().add_view(request, form_url, extra_context)
#
#     # def change_view(self, request, object_id, form_url='', extra_context=None):
#     #     extra_context = extra_context or {}
#     #     extra_context['show_save_and_add_another'] = False
#     #     # or
#     #     extra_context['really_hide_save_and_add_another_damnit'] = True
#     #     return super().change_view(request, object_id,
#     #                                                  form_url, extra_context=extra_context)
#
#     def save_model(self, request, obj, form, change):
#         """ store the select country for use in get_field_queryset """
#         self.selected_match = obj.match_id
#         return super().save_model(request, obj, form, change)
#
#     def get_field_queryset(self, db, db_field, request):
#         """ filter the City queryset by selected country """
#         queryset = super().get_field_queryset(db, db_field, request)
#         if db_field.name == 'player_id':
#             if queryset is None:
#                 # If "ordering" is not set on the City admin, get_field_queryset returns
#                 # None, so we have to get it ourselves. See original source:
#                 # github.com/django/django/blob/2.1.5/django/contrib/admin/options.py#L209
#                 queryset = Player.objects.all()
#             # Filter by country
#             queryset = queryset.filter(Q(club=self.selected_match.home_team) | Q(club=self.selected_match.guest_team))
#         return queryset
# # Q(club=match.home_team) | Q(club=match.guest_team)

class TeamAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'player_id', 'tour_number_start', 'tour_number_end', 'is_captain']

class TourAdmin(admin.ModelAdmin):

    list_display = ['number', 'name', 'start_time', 'supposed_end_time', 'end_time', 'season']

class ResultProfilesAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'tour_number', 'points']


class ResultPlayersAdmin(admin.ModelAdmin):

    list_display = ['player_id', 'tour_number', 'points']


class MissMatchAdmin(admin.ModelAdmin):

    list_display = ['match_id', 'player_id']

class TeamTemporaryAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'player_id', 'transfer', 'timeout']

class CaptainAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'tour_number', 'player_id' ]
    list_filter = ['user_id', 'tour_number']


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
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.site_header = 'Russian Fantasy Hockey'
