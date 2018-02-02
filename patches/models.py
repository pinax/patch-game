from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


class ActivityItem(models.Model):
    """
    Items generated for an activity based on a factory.
    """
    activity = models.CharField(max_length=150, default="guess-the-patch")
    data = JSONField()
    created_at = models.DateTimeField(default=timezone.now)


class ActivitySession(models.Model):
    """
    A user's session for a given activity
    """
    activity = models.CharField(max_length=150, default="guess-the-patch")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class SessionItem(models.Model):
    """
    For a user's session on an activity and each item in that session, collect
    data on attempts and streaks.
    """
    item = models.ForeignKey(ActivityItem, on_delete=models.CASCADE)
    session = models.ForeignKey(ActivitySession, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)


class ItemShowing(models.Model):
    """
    Each time an item in a session is shown to the user, record that information
    with this model
    """
    item = models.ForeignKey(SessionItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Response(models.Model):
    """
    The response a user records for each showing of an Item.
    """
    item = models.ForeignKey(ItemShowing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    answer = JSONField(blank=True)
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(100),
        ]
    )

    def save(self, *args, **kwargs):
        if self.answer["answer"] == self.item.item.item.data["answer"]:
            self.score = 100
        else:
            self.score = 0
        return super().save(*args, **kwargs)
