from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage


DEFAULT_BUDGET = 100


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team_name = models.CharField(max_length=30, null=True, blank=True, unique=True)
    budget = models.FloatField(default=DEFAULT_BUDGET, editable=False)
    changes_count = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0, blank=False, null=False, editable=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user_id=instance)
            email = EmailMessage(
                'Вы успешно зарегистрировались',
                'Спасибо за регистрацию, ваше имя пользователя: {}, обязательно ознакомьтесь с правилами: https://fantasyhockey.ru/rules/.\n'
                'Войти можно здесь: https://fantasyhockey.ru/accounts/login/'.format(instance.username),
                to=[instance.email]
            )
            email.send()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return str(self.user_id)


class AdBanners(models.Model):

    name = models.CharField(max_length=120, null=False, blank=False)
    start_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=False, null=False)
    end_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=False, null=False)
    small_image = models.ImageField(upload_to='banners/', blank=False, null=False, help_text='Resolution 414 x 50 px')
    medium_image = models.ImageField(upload_to='banners/', blank=False, null=False, help_text='Resolution 800 x 80 px')
    large_image = models.ImageField(upload_to='banners/', blank=False, null=False, help_text='Resolution 1140 x 90 px')
    link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'AdBanner'
        verbose_name_plural = 'AdBanners'


