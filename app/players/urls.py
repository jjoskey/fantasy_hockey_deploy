from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'send_players_list/$', views.send_players_list , name='send_players_list'),
    url(r'receive_player_id_to_add/$', views.receive_player_id_to_add , name='receive_player_id_to_add'),
    url(r'receive_player_id_to_unactivate/$', views.receive_player_id_to_unactivate, name='receive_player_id_to_unactivate'),
    url(r'save_team/$', views.save_team, name='save_team'),
    url(r'cancel_transfers/$', views.cancel_transfers, name='cansel_transfers'),
    url(r'receive_captains_id/$', views.receive_captains_id, name='receive_captains_id')
]