from rest_framework import permissions


class IsOwnerOrPublic(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view it or edit
    it, if it is not public.
    Assumes the model instance has an `owner` and a `public` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.public or obj.owner == request.user
