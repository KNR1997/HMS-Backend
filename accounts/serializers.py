# Client User Serializer
from rest_framework import serializers

from accounts.models import User


class ClientUserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['permissions', 'role']

    # def get_permissions(self, obj):
    #     # Return only the group names
    #     return obj.groups.values_list('name', flat=True)

    def get_role(self, obj):
        # Return only the group names
        return 'super_admin'

    def get_permissions(self, obj):
        # Return only the group names
        return ['super_admin']

class MeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['name']

    def get_name(self, obj):
        return obj.get_full_name()
