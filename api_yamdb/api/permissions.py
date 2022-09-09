from rest_framework import permissions


class IsAuthorOrAdminPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or obj.is_staff
