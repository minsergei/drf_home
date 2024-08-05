from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверка на модератора."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    """Проверка на владельца."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
