from django.contrib.auth.models import User
from django.db import models


class Session(models.Model):
    """
    Session model.
    """
    name = models.CharField(max_length=255)

    # Relations
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sessions')

    class Meta:
        db_table = 'session'


class Review(models.Model):
    """
    Review model.
    """
    class StateChoices(models.Choices):
        OPENED = 'opened'
        CLOSED = 'closed'

    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    state = models.CharField(choices=StateChoices.choices)

    # Relations
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'review'
