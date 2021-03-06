from django.conf.urls import url, include
from django.contrib import admin
from . import views
from freeze_and_count.views import render_freeze_and_count
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.render_home_page, name='home'),
    url(r"^accounts/", include("accounts.urls", namespace="accounts")),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^loggedin/$", views.LoggedinPage.as_view(), name="loggedin"),
    url(r"^thanks/$", views.ThanksPage.as_view(), name="thanks"),
    url(r"^play/$", views.render_play_page, name="play"),
    url(r"^api_players/", include("players.urls", namespace="players")),
    url(r"^freeze_and_count/$", render_freeze_and_count, name="freeze_and_count"),
    url(r'^api_freeze_and_count/', include('freeze_and_count.urls', namespace='freeze_and_count_api')),
    url(r'^leaders/$', views.render_leaders, name="leaders"),
    url(r'^users_team/(?P<user_id>\d+)/$', views.render_user_team),
    url(r'^rules/$', views.render_rules, name='rules')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
