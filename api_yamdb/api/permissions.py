from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Недостаточно прав на изменения'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)
