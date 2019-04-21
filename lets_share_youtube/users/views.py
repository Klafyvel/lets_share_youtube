from django.contrib.auth.models import User

from rest_framework import status, viewsets, permissions

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows User management"""

    serializer_class = UserSerializer
    lookup_field = "username"
    lookup_value_regex = "\w+"
    permission_classes = [permissions.AllowAny]

    queryset = User.objects.all()
