from rest_framework import serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from accounts.selectors import admin_list
from common.utils import parse_search_query, get_paginated_response


class AdminListApi(APIView):
    permission_classes = [IsAdminUser]

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True)
        email = serializers.CharField(required=True)
        is_active = serializers.CharField(required=True)
        # permissions = serializers.SerializerMethodField()

        # @staticmethod
        # def get_permissions(obj):
        #     # Return a list of permission types for the user
        #     return [
        #         {"name": permission.permission_type, "index": index}
        #         for index, permission in enumerate(obj.permissions.all())
        #     ]

    def get(self, request):
        # Extract `search` query parameter
        query_params = request.query_params
        search_query = query_params.get("search", None)

        # Parse `search` using the utility function
        filters = parse_search_query(search_query)

        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data={**request.query_params, **filters})
        filters_serializer.is_valid(raise_exception=True)

        admins = admin_list(filters=None)

        # Apply pagination
        return get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=admins,
            request=request,
        )
