from django.db import models
from django.contrib.auth.models import User
# from django.conf.urls import *
from django.conf import settings
# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)


    def __str__(self):
        return self.title
