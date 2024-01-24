from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешение только для владельца объекта (корзины)
        return obj.user == request.user
