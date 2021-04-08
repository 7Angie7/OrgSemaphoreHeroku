import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class Semaphore(models.Model):
    STATUS = (
        ('Ready', 'Ready'),
        ('Busy', 'Busy'),
    )

    name = models.CharField(max_length=200, null=True)
    time = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    controlUrl = models.UUIDField(default=uuid.uuid4)
    lastQueueNum = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class QueueClient(models.Model):
    semap = models.ForeignKey(Semaphore, on_delete=models.CASCADE, null=True)
    device = models.CharField(max_length=200, null=True)
    queueNum = models.IntegerField(null=True)
    clientName = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.device
