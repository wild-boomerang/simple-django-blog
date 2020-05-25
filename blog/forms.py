from django import forms
from .models import Post, Comment, Profile
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
        fields = ('username', 'first_name', 'email')

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
