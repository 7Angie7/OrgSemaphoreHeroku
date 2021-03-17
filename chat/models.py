from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Semaphore(models.Model):
    name = models.CharField(max_length=200, null=True)
    time = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
