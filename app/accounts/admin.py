from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):

    # fields = ['team_name', 'budget'] # изменяет порядок для detail view

    list_display = ['user_id', 'team_name', 'budget', 'changes_count', 'points', 'pk']

    # search_fields = ['team_name'] # добавляет поля для поиска

    # list_filter = ['points'] # добавляет доп. фильтры

    # list_editable = ['budget'] # делает поле редактируемым, даже если в базе оно нередактируемо




admin.site.register(Profile, ProfileAdmin)