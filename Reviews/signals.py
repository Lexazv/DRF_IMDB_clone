from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from .models import Review, Like


@receiver(post_save, sender=Review)
def update_film_data(sender, instance, created, **kwargs):
    """ Update film data after review created """
    if created:
        film = instance.film
        if film.reviews_number != 0:
            film.avg_rate = (film.avg_rate + instance.rate) / 2
        else:
            film.avg_rate = instance.rate
        film.reviews_number += 1
        film.save()


@receiver(post_save, sender=Like)
def increase_likes_number(sender, instance, created, **kwargs):
    if created:
        instance.review.likes_amount += 1
        instance.review.save()


@receiver(pre_delete, sender=Like)
def decrease_likes_number(sender, instance, using, **kwargs):
    instance.review.likes_amount -= 1
    instance.review.save()
