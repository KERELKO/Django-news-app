from django.conf import settings
from rest_framework import serializers

User = settings.AUTH_USER_MODEL


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']
