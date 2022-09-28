from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the reminder.
        return obj.owner == request.user


# http -a Sam:@Zoester123 POST http://127.0.0.1:8000/reminder/ reminder="a second test reminder for Sam"
# {
#     "owner": {
#         "id": 1,
#         "name": "Sam"
#     },
#     "reminder": "testing testing 123"
# }