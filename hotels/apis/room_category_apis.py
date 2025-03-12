from django.db import transaction
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.selectors import user_get
from common.utils import parse_search_query, get_paginated_response
from hotels.models import Room
from hotels.selectors import room_get, room_category_list, room_category_get_by_slug
from hotels.services.room_category_services import room_category_create, room_category_update, room_category_delete
from hotels.services.room_services import room_update, room_delete


class RoomCategoryListApi(APIView):
    permission_classes = [AllowAny]

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True)
        name = serializers.CharField(required=True)
        slug = serializers.CharField(required=True)
        image =serializers.JSONField(required=True)
        description = serializers.CharField(required=True)
        capacity = serializers.IntegerField(required=True)
        price_per_night = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)

    def get(self, request):
        # Extract `search` query parameter
        query_params = request.query_params
        search_query = query_params.get("search", None)

        # Parse `search` using the utility function
        filters = parse_search_query(search_query)

        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data={**request.query_params, **filters})
        filters_serializer.is_valid(raise_exception=True)

        room_categories = room_category_list(filters=filters_serializer.validated_data)

        # Apply pagination
        return get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=room_categories,
            request=request,
        )


class AdminRoomCategoryDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        slug = serializers.CharField()
        image = serializers.JSONField()
        description = serializers.CharField()
        capacity = serializers.IntegerField()
        price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get(self, request, slug):
        room_category = room_category_get_by_slug(slug)

        if room_category is None:
            raise Http404

        data = self.OutputSerializer(room_category).data

        return Response(data)


class PublicRoomCategoryDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        slug = serializers.CharField()
        image = serializers.JSONField()
        description = serializers.CharField()
        capacity = serializers.IntegerField()
        price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2)
        room_numbers = serializers.SerializerMethodField()

        def get_room_numbers(self, obj):
            # Fetch all rooms associated with the RoomCategory
            rooms = Room.objects.filter(category=obj)
            # Extract and return the room numbers
            return [room.room_number for room in rooms]

    def get(self, request, slug):
        room_category = room_category_get_by_slug(slug)

        if room_category is None:
            raise Http404

        data = self.OutputSerializer(room_category).data

        return Response(data)

class RoomCategoryCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        slug = serializers.CharField(required=True)
        image = serializers.JSONField()
        description = serializers.CharField(required=True, allow_null=True, allow_blank=True)
        capacity = serializers.CharField(required=True)
        price_per_night = serializers.CharField(required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room_category = room_category_create(
            **serializer.validated_data
        )

        # Note: This shows a possible reusability for serializers between APIs
        # Usually, this is how we approach things, when building APIs at first
        # But at the very moment when we need to make a change to the output,
        # that's specific to this API, we'll introduce a separate OutputSerializer just for this API
        data = RoomCategoryListApi.OutputSerializer(room_category).data

        return Response(data)


class RoomCategoryUpdateApi(APIView):

    @transaction.atomic
    def put(self, request, slug):
        serializer = RoomCategoryCreateApi.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_get(user_id=serializer.validated_data.get('created_by'))
        room_category = room_category_get_by_slug(slug)

        if room_category is None:
            raise Http404

        room_category = room_category_update(room_category=room_category, data=serializer.validated_data, updated_by=user)

        # Note: This shows a possible reusability for serializers between APIs
        # Usually, this is how we approach things, when building APIs at first
        # But at the very moment when we need to make a change to the output,
        # that's specific to this API, we'll introduce a separate OutputSerializer just for this API
        data = AdminRoomCategoryDetailApi.OutputSerializer(room_category).data

        return Response(data)


class RoomCategoryDeleteApi(APIView):
    @staticmethod
    def delete(request, room_category_id: str):
        room_category_delete(room_category_id=room_category_id)

        return Response(
            {"detail": "Room Category successfully deleted."},
            status=status.HTTP_204_NO_CONTENT  # 204 for successful delete with no content
        )
