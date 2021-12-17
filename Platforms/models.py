from django.db import models
from django.contrib.auth.models import User


class Platform(models.Model):

    name = models.CharField(max_length=50, unique=True)
    link = models.URLField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    added_on = models.DateField(auto_now_add=True)
    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name
