
from email import message
from rest_framework import permissions
# from users.models import Users
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = 'Permission Denied'
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
