from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.

class Group(models.Model):
    group_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    user_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    passpot_seriya = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
