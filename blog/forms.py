from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Post, Comment, Profile, Message
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'last_name')

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_repeat']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_repeat']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {'message': ""}


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')

    date_of_birth = forms.DateField()

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']):
            raise forms.ValidationError('email already registered!')
        return cd['email']

    # def clean_date_of_birth(self):
    #     cd = self.cleaned_data
    #     if cd['date_of_birth'] > timezone.datetime(timezone.get_current_timezone()):
    #         raise forms.ValidationError('Date of birth is invalid!.')
    #     return cd['date_of_birth']
