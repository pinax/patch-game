from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


class Showing(models.Model):
    """
    Each time an item in a session is shown to the user, record that information
    with this model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def user_state(self):
        return UserState.state_for_user(self.user)


class Response(models.Model):
    """
    The response a user records for each showing of an Item.
    """
    item = models.ForeignKey(Showing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    answer = JSONField(blank=True)
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(100),
        ]
    )

    def save(self, *args, **kwargs):
        if self.answer["answer"] == self.item.data["answer"]:
            self.score = 100
        else:
            self.score = 0
        self.item.user_state.store_last_correct(self.item.data["answer"])
        return super().save(*args, **kwargs)


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
