from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
import uuid


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.caption}'


class User(AbstractUser):
    name = models.CharField(
        max_length=100,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        null=True,
    )

    bio = models.TextField()

    creator_of_event = models.BooleanField(default=True, null=True)

    avatar = ResizedImageField(size=[250, 250], default='avatar.jpg')

    website = models.URLField(max_length=500, null=True, blank=True)

    created = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    # id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Cause(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=800, null=True, blank=True)

    image = ResizedImageField(size=[250, 250], default='thelogo.PNG')

    location = models.URLField()  # Location from Google Maps
    followers = models.ManyToManyField(
        User,
        blank=True,
        related_name='causes',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    likes = models.ManyToManyField(User, related_name='cause_likes')
    tags = models.ManyToManyField(Tag, related_name='cause_tags')

    def total_cause_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True, )
    cause = models.ForeignKey(Cause, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='event_creator')
    image = ResizedImageField(size=[500, 500], default='thelogo.PNG')
    location = models.URLField()
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name='events',
    )
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    likes = models.ManyToManyField(User, related_name='event_likes')
    tag = models.ManyToManyField(Tag, related_name='event_tags')

    #
    # id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def total_event_likes(self):
        return self.likes.count()

    def __str__(self):
        try:
            return str(self.cause) + ' --- ' + str(self.creator.username) + ' --- ' + str(self.title)
        except AttributeError:
            return str(self.cause) + ' --- ' + str(self.title)


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_comments')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    text = models.TextField(max_length=400)
    created_on = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.name)

    @property
    def number_of_comments(self):
        return Comment.objects.filter(event=self).count()
