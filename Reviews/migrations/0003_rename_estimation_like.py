# Generated by Django 3.2.7 on 2021-12-16 13:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reviews', '0002_estimation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Estimation',
            new_name='Like',
        ),
    ]
