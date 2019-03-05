"""fantasy_hockey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from freeze_and_count.views import render_freeze_and_count

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r"^accounts/", include("accounts.urls", namespace="accounts")),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^loggedin/$", views.LoggedinPage.as_view(), name="loggedin"),
    url(r"^thanks/$", views.ThanksPage.as_view(), name="thanks"),
    url(r"^play/$", views.PlayPage.as_view(), name="play"),
    url(r"^api_players/", include("players.urls", namespace="players")),
    url(r"^freeze_and_count/$", render_freeze_and_count, name="freeze_and_count"),
    url(r'^api_freeze_and_count/', include('freeze_and_count.urls', namespace='freeze_and_count_api')),
    url(r'^leaders/$', views.render_leaders, name="leaders")
]
