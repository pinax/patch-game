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
        return super().save(*args, **kwargs)


class UserState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField(default=dict)
