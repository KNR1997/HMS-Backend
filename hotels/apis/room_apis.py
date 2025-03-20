from django.db import transaction
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.selectors import user_get
from common.utils import parse_search_query, get_paginated_response
from hotels.selectors import room_list, room_get, room_get_by_room_number
from hotels.services.room_services import room_create, room_update, room_delete


class RoomListApi(APIView):
    permission_classes = [AllowAny]

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        category = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True)
        category = serializers.CharField(required=True)
        room_number = serializers.CharField(required=True)
        is_available = serializers.BooleanField(required=True)
        price = serializers.DecimalField(required=True, source='category.price_per_night', max_digits=10, decimal_places=2)
        image = serializers.JSONField(required=True, source='category.image')

    def get(self, request):
        # Extract `search` query parameter
        query_params = request.query_params
        search_query = query_params.get("search", None)

        # Parse `search` using the utility function
        filters = parse_search_query(search_query)

        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data={**request.query_params, **filters})
        filters_serializer.is_valid(raise_exception=True)

        rooms = room_list(filters=filters_serializer.validated_data)

        # Apply pagination
        return get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=rooms,
            request=request,
        )


class RoomDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        category = serializers.CharField()
        room_number = serializers.CharField()
        is_available = serializers.BooleanField()

    def get(self, request, room_number):
        room = room_get_by_room_number(room_number)

        if room is None:
            raise Http404

        data = self.OutputSerializer(room).data

        return Response(data)


class RoomCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        category_id = serializers.UUIDField(required=True)
        room_number = serializers.CharField(required=True)
        is_available = serializers.BooleanField(required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = room_create(
            **serializer.validated_data
        )

        # Note: This shows a possible reusability for serializers between APIs
        # Usually, this is how we approach things, when building APIs at first
        # But at the very moment when we need to make a change to the output,
        # that's specific to this API, we'll introduce a separate OutputSerializer just for this API
        data = RoomListApi.OutputSerializer(room).data

        return Response(data)


class RoomUpdateApi(APIView):

    @transaction.atomic
    def put(self, request, room_number):
        serializer = RoomCreateApi.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_get(user_id=serializer.validated_data.get('created_by'))
        room = room_get_by_room_number(room_number)

        if room is None:
            raise Http404

        room = room_update(room=room, data=serializer.validated_data, updated_by=user)

        # Note: This shows a possible reusability for serializers between APIs
        # Usually, this is how we approach things, when building APIs at first
        # But at the very moment when we need to make a change to the output,
        # that's specific to this API, we'll introduce a separate OutputSerializer just for this API
        data = RoomDetailApi.OutputSerializer(room).data

        return Response(data)


class RoomDeleteApi(APIView):
    @staticmethod
    def delete(request, room_id: str):
        room_delete(room_id=room_id)

        return Response(
            {"detail": "Room successfully deleted."},
            status=status.HTTP_204_NO_CONTENT  # 204 for successful delete with no content
        )
