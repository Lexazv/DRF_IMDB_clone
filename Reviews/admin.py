from django.contrib import admin

from .models import Review, Like


admin.site.register([Review, Like])
