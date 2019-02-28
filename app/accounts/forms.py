from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields["username"].label = "Ваш никнейм"
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повторите пароль"


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('team_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_name'].label = "Назоваите вашу команду"