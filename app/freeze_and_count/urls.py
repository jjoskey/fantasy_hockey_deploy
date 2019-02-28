from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'', views.render_freeze_and_count, name='render'),
    url(r'send_last_freeze/$', views.send_last_freeze, name='send_last_freeze'),
    url(r'receive_freeze_data/$', views.receive_freeze_data, name='receive_freeze_data'),
    url(r'count_and_save_points/$', views.count_and_save_points, name='count_and_save_points'),
    url(r'add_changes_to_all_profile/$', views.add_changes_using_data, name='add_changes_to_all_profile'),
]