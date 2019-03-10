from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()
        # exclude = ('email.help_text',)
        # help_texts = {
        #     'username': None,
        #     'email': None
        # }

    email = forms.EmailField(max_length=40)

    username = forms.RegexField(
        min_length=5,
        max_length=30,
        regex=r'^[a-zA-z0-9]+$',
        error_messages={
            'invalid': ("Можно использовать только 30 символов: латинские буквы и цифры")
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields["username"].label = "Имя пользователя"
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повторите пароль"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        # if '@' not in email:
        #     print('Yes')
        #     raise forms.ValidationError(u'Вот такие дела')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Пользователь с таким e-mail уже существует')

        return email


class RestorePassword(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('email',)

    email = forms.EmailField(max_length=40)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('team_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

