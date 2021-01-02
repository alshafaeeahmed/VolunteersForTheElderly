from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User

from .models import Profile, Post, Comment


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254, help_text='Required field')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

#bild the user form
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required field')

    class Meta:
        model = User
        fields = ['email']



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['status_info', 'profile_photo', 'is_volunteer', 'phone_number']


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_text', 'post_picture']


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )


class urgent_request(forms.Form):
    def __init__(self, *args, **kwargs):
        super(urgent_request, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.form_action = '/contact'

        self.helper.add_input(Submit('submit', 'Submit'))

    email = forms.EmailField(max_length=254)
    message = forms.CharField(max_length=254, widget=forms.Textarea)
