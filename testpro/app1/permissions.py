from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print request.user
        users = [us.user for us in obj.authors.all()]
        print users
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user in users:
            return True
        return False