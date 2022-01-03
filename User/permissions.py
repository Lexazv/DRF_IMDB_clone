from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class NotAuthentficated(BasePermission):

    def has_permission(self, request, view):
        return isinstance(request.user, AnonymousUser)
