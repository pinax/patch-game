import time

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from pinax.points.models import award_points


class Topic(models.Model):
    """
    An entity object that provides a way to have categories of items.
    """
    name = models.CharField(max_length=500)


class Showing(models.Model):
    """
    Each time an item is shown to the user, record that information
    with this model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    topics = models.ManyToManyField(Topic)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for name in self.data.get("topics", []):
            topic, _ = Topic.objects.get_or_create(name=name)
            self.topics.add(topic)

    @property
    def user_state(self):
        return UserState.state_for_user(self.user)


class Response(models.Model):
    """
    The response a user records for each showing of an Item.
    """
    showing = models.OneToOneField(Showing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    answer = JSONField(blank=True)
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(100),
        ]
    )

    def save(self, *args, **kwargs):
        if self.answer["answer"] == self.showing.data["answer"]:
            self.score = 100
        else:
            self.score = 0
        super().save(*args, **kwargs)
        if self.score == 100:
            self.showing.user_state.store_last_correct(self.showing.data["answer"])
            apv = award_points(self.showing.user, 5)
        else:
            apv = award_points(self.showing.user, -1)
        self.showing.user_state.store("last_points", apv.points)
        self.showing.user_state.store("last_points_awarded", time.time())


class UserState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField(default=dict)

    @classmethod
    def state_for_user(cls, user):
        state, _ = cls.objects.get_or_create(user=user)
        return state

    def store(self, key, value):
        self.data[key] = value
        self.save()

    def store_last_correct(self, value):
        if "last_correct" not in self.data:
            self.data["last_correct"] = {}
        self.data["last_correct"].update({value: timezone.now().isoformat()})
        self.save()
