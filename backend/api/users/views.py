from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.apps.users.models import CustomUser as User

from .serializers import UserSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
