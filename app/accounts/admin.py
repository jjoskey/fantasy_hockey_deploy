from django.contrib import admin
from .models import Profile, AdBanners


class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'team_name', 'budget', 'changes_count', 'points', 'pk']


class AdBannersAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'small_image', 'medium_image', 'large_image', 'link']


admin.site.register(AdBanners, AdBannersAdmin)
# admin.site.register(Profile, ProfileAdmin)