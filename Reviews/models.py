from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class GeneralInfo(models.Model):

    added_on = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:

        abstract = True


class Review(GeneralInfo, models.Model):

    rate = models.PositiveSmallIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )
    updated_on = models.DateTimeField(auto_now=True)
    likes_amount = models.IntegerField(default=0)
    description = models.TextField(max_length=500)
    film = models.ForeignKey(
        'Films.Film', on_delete=models.CASCADE, related_name='reviews'
    )

    def __str__(self) -> str:
        return f'{self.owner} - {self.film.title} - {self.rate}'


class Like(GeneralInfo, models.Model):

    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.owner}'
