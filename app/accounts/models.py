from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage


DEFAULT_BUDGET = 16


# class User(auth.models.User, auth.models.PermissionsMixin):
#
#     def __str__(self):
#         return "@{}".format(self.username)


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team_name = models.CharField(max_length=30, null=True, blank=True)
    budget = models.FloatField(default=DEFAULT_BUDGET)
    changes_count = models.PositiveIntegerField(default=0)
    refresh_changes = models.BooleanField(editable=False, default=False)
    points = models.PositiveIntegerField(default=0, blank=False, null=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user_id=instance)
            email = EmailMessage(
                'Вы успешно зарегистрировались',
                'Спасибо за регистрацию, ваше имя пользователя: {}, обязательно ознакомьтесь с правилами: https://fantasyhockey.ru/rules/.'.format(instance.username),
                to=[instance.email]
            )
            email.send()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return str(self.user_id)

