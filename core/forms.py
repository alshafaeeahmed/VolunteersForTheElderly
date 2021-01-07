from django import forms
from django.contrib.auth.models import User

from .models import Profile, Post, Comment, UrgentRequest, PageUpdate, contact_us


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254, help_text='Required field')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# the user form
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required field')

    class Meta:
        model = User
        fields = ['email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['status_info', 'profile_photo', 'is_volunteer', 'phone_number', 'gender', 'address', 'rating',
                  'is_active']


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_text', 'post_picture']


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']


class PageUpdate(forms.ModelForm):
    class Meta:
        model = PageUpdate
        fields = '__all__'


class Contact_UsForm(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = '__all__'


class UrgentRequestForm(forms.ModelForm):
    class Meta:
        model = UrgentRequest
        fields = '__all__'
