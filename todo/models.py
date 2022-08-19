from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(default=now, editable=False)
    deadline = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
