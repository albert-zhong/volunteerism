from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MyUser
        fields = ('email', 'first_name', 'last_name')


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')