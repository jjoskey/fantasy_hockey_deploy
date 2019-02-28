from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from players.models import Player
import json
from django.http import JsonResponse
from django.core import serializers


class LoggedinPage(TemplateView):
    template_name = 'loggedin.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    template_name = "index.html"


class PlayPage(TemplateView):

    template_name = "play.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['players'] = serializers.serialize('json', Player.objects.all())
    #     print(context['players'])
    #
    #     return context


