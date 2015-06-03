from rest_framework import permissions
from models import *


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return obj.authors.get(user=request.user) is not None
        except:
            return False


class IsAuthorBooksOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        auth = Author.objects.get(id=view._get_kwa().get('id'))
        if request.user == auth.user:
            return True
        return False


class IsBookAuthorsOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        kwa = view._get_kwa()
        auth = Author.objects.get(pk=kwa.get('pk'))
        if auth.user == request.user:
            return True
        return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False