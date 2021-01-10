from django import forms
from django.contrib.auth.models import User

from .models import Profile, Post, Comment, UrgentRequest, PageUpdate, Contact_us, Site_Info


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
        labels = {
            'post_text': 'תוכן סיכום',
            'post_picture': 'תמונה',
            'status_info': 'סטטוס',
            'is_volunteer': 'הפוך למתנדב',
            'phone_number': 'מספר טאלפון',
            'gender': 'מין',
            'address': 'כתובת',
            'rating': 'דרוג',
            'is_active': 'פעיל',
        }


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_text', 'post_picture']
        labels = {
            'post_text': 'תוכן סיכום',
            'post_picture': 'הוסף תמונה',
        }


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {
            'comment_text': 'תגובה',

        }


class PageUpdate(forms.ModelForm):
    class Meta:
        model = PageUpdate
        fields = '__all__'


class Site_Info(forms.ModelForm):
    class Meta:
        model = Site_Info
        fields = '__all__'


class Contact_UsForm(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = '__all__'


class UrgentRequestForm(forms.ModelForm):
    class Meta:
        model = UrgentRequest
        fields = '__all__'
