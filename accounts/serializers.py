# Client User Serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class ClientUserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['permissions', 'role', 'username']

    # def get_permissions(self, obj):
    #     # Return only the group names
    #     return obj.groups.values_list('name', flat=True)

    def get_role(self, obj):
        # Return only the group names
        return 'super_admin' if obj.is_superuser else 'store_owner'

    def get_permissions(self, obj):
        # Return only the group names
        return ['super_admin'] if obj.is_superuser else ['store_owner']


class MeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['name']

    def get_name(self, obj):
        return obj.get_full_name()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
