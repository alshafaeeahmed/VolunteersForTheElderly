from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(default='default.jpg', upload_to='profile_photos')
    status_info = models.CharField(default="Enter status", max_length=1000)
    is_volunteer = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format: '+0000000000'")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_text = models.CharField(max_length=2000)
    post_picture = models.FileField(default="default.jpg", upload_to='post_picture')


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    following_user = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.following_user.username


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    follower_user = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.follower_user.username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment_text = models.CharField(default="Enter Comment Here", max_length=2000)

#for urgent recquest page

class Message(models.Model):
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=300)