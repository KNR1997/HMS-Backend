from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.selectors import user_list
from common.utils import parse_search_query, get_paginated_response


class UserListApi(APIView):
    # permission_classes = [AllowAny]

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        email = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True)
        email = serializers.CharField(required=True)
        # is_staff = serializers.CharField(required=True)
        is_active = serializers.CharField(required=True)

    def get(self, request):
        # Extract `search` query parameter
        query_params = request.query_params
        search_query = query_params.get("search", None)

        # Parse `search` using the utility function
        filters = parse_search_query(search_query)

        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data={**request.query_params, **filters})
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=None)

        # Apply pagination
        return get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
        )


class UserDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        username = serializers.CharField(required=False)
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)
        is_admin = serializers.BooleanField(required=True)

    def get(self, request):
        # Get the currently authenticated user
        requested_user = request.user

        data = self.OutputSerializer(requested_user).data

        return Response(data)
