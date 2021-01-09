from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

ADDRESS_CHOICES = (
    ('BeerSheba', 'באר שבע'),
    ('TelAviv', 'תל אביב'),
    ('Ashdod', 'אשדוד'),
    ('Jerusalem', 'ירושלים'),
    ('Haifa', 'חיפה'),
    ('Jaffa', 'יפו'),
    ('Acre', 'עכו'),
    ('Nazareth', 'נצרת'),
    ('Lod', 'לוד'),
    ('Arad', 'ערד'),
    ('Dimona', 'דימונה'),
    ('Rishon Lezion', 'רישון לציון'),
    ('Ashkelon', 'אשקלון')

)
GENDER_CHOICES = (
    ('זכר', 'זכר'),
    ('נקבה', 'נקבה'),
)
Status_Info_CHOICES = (
    ('זמין', 'זמין'),
    ('לא זמין', 'לא זמין'),
)
Rating_CHOICES = (
    ('טוב', 'טוב'),
    ('בסדר', 'בסדר'),
    ('טוב מאוד', 'טוב מאוד'),
    ('לא טוב', 'לא טוב'),
    ('מצויין', 'מצויין'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(default='default.jpg', upload_to='profile_photos')
    status_info = models.CharField(max_length=10, choices=Status_Info_CHOICES, default='זמין')
    is_volunteer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format: '+0000000000'")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='זכר')
    address = models.CharField(max_length=40, choices=ADDRESS_CHOICES, default='BeerSheba')
    rating = models.CharField(max_length=10, choices=Rating_CHOICES, default='good')


    def __str__(self):
        return f'{self.user.username} Profile'


class PageUpdate(models.Model):
    subject = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "PageUpdate"

    def __str__(self):
        return self.subject


class Site_Info(models.Model):
    subject = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Site_Info"

    def __str__(self):
        return self.subject


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_text = models.CharField(max_length=2000)
    post_picture = models.FileField(default="default.jpg", upload_to='post_picture')
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    def number_of_likes(self):
        return self.likes.count()


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


# for urgent request page

class Message(models.Model):
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=300)


# add contact fileds
class Contact_us(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact_us"

    def __str__(self):
        return self.name + "-" + self.email


# add urgent_request fileds
class UrgentRequest(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "UrgentRequest"

    def __str__(self):
        return self.name