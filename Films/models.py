from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):

    title = models.CharField(max_length=50, unique=True)
    director = models.CharField(max_length=50)
    avg_rate = models.FloatField(default=0)
    reviews_number = models.IntegerField(default=0)
    released_on = models.DateField(max_length=50)
    description = models.TextField(max_length=500)
    added_on = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    platform = models.ForeignKey(
        'Platforms.Platform', on_delete=models.CASCADE, related_name='films'
    )

    def __str__(self) -> str:
        return self.title
