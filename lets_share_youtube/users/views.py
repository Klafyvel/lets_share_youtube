from django.contrib.auth.models import User

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows User management"""

    serializer_class = UserSerializer
    lookup_field = "username"
    lookup_value_regex = "\w+"
    permission_classes = [permissions.AllowAny]

    queryset = User.objects.all()


@api_view(["GET"])
@permission_classes((AllowAny,))
def am_i_logged(request):
    if request.user.is_authenticated:
        return Response({"user": request.user.username}, status=status.HTTP_200_OK)
    return Response({"too_bad": True}, status=status.HTTP_400_BAD_REQUEST)
