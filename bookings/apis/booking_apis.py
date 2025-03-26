from django.db import transaction
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.selectors import booking_list, booking_get_by_booking_number, my_booking_list
from bookings.services.booking_services import process_booking, booking_update, booking_delete, \
    process_booking_by_customer
from common.utils import parse_search_query, get_paginated_response


class ProcessBookingApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.UUIDField(required=True)
        check_in = serializers.CharField(required=True)
        check_out = serializers.CharField(required=True)
        booking_items = serializers.ListField(required=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()

    @transaction.atomic
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = process_booking(**serializer.validated_data)

        return Response(self.OutputSerializer(booking).data)


class ProcessBookingFromAdminApi(APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        customer_name = serializers.CharField(required=True)
        customer_id_number = serializers.CharField(required=True)
        check_in = serializers.CharField(required=True)
        check_out = serializers.CharField(required=True)
        booking_items = serializers.ListField(required=True)
        status = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()

    @transaction.atomic
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = process_booking(**serializer.validated_data)

        return Response(self.OutputSerializer(booking).data)


class ProcessBookingByCustomerApi(APIView):
    # permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        customer_name = serializers.CharField(required=True)
        customer_id_number = serializers.CharField(required=True)
        check_in = serializers.CharField(required=True)
        check_out = serializers.CharField(required=True)
        booking_items = serializers.ListField(required=True)
        status = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()

    @transaction.atomic
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        booking = process_booking_by_customer(
            user=user,
            **serializer.validated_data
        )

        return Response(self.OutputSerializer(booking).data)


class BookingListApi(APIView):
    # permission_classes = [AllowAny]

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        customer_name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True)
        booking_number = serializers.IntegerField(required=True)
        customer_name = serializers.CharField(required=True)
        check_in = serializers.DateField(required=True)
        check_out = serializers.DateField(required=True)
        total_price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
        status = serializers.CharField(required=True)

    def get(self, request):
        # Extract `search` query parameter
        query_params = request.query_params
        search_query = query_params.get("search", None)

        # Parse `search` using the utility function
        filters = parse_search_query(search_query)

        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data={**request.query_params, **filters})
        filters_serializer.is_valid(raise_exception=True)

        bookings = booking_list(filters=filters_serializer.validated_data)

        # Apply pagination
        return get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=bookings,
            request=request,
        )


class MyBookingListApi(APIView):
    # permission_classes = [AllowAny]

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True)
        booking_number = serializers.IntegerField(required=True)
        customer_name = serializers.CharField(required=True)
        check_in = serializers.DateField(required=True)
        check_out = serializers.DateField(required=True)
        total_price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
        status = serializers.CharField(required=True)

    def get(self, request):
        # Extract `search` query parameter
        query_params = request.query_params
        search_query = query_params.get("search", None)

        # Parse `search` using the utility function
        filters = parse_search_query(search_query)

        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data={**request.query_params, **filters})
        filters_serializer.is_valid(raise_exception=True)

        user = request.user

        bookings = my_booking_list(
            filters=filters_serializer.validated_data,
            user=user
        )

        # Apply pagination
        return get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=bookings,
            request=request,
        )


class RoomDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    room_number = serializers.CharField(source='room.room_number')
    room_category_name = serializers.CharField(source='room.category.name')
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2)


class BookingDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        booking_number = serializers.CharField()
        user = serializers.CharField(required=True)
        check_in = serializers.DateField(required=True)
        check_out = serializers.DateField(required=True)
        total_price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
        status = serializers.CharField(required=True)
        rooms = RoomDetailSerializer(many=True, source='booking_items')

    def get(self, request, booking_number):
        booking = booking_get_by_booking_number(booking_number=booking_number)

        if booking is None:
            raise Http404

        data = self.OutputSerializer(booking).data

        return Response(data)


class BookingUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        status = serializers.CharField(required=False)

    def put(self, request, booking_number):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        booking = booking_get_by_booking_number(booking_number=booking_number)

        if booking is None:
            raise Http404

        booking = booking_update(booking=booking, data=serializer.validated_data)

        data = ProcessBookingApi.OutputSerializer(booking).data

        return Response(data)


class BookingDeleteApi(APIView):
    @staticmethod
    def delete(request, booking_id: str):
        booking_delete(booking_id=booking_id)

        return Response(
            {"detail": "Booking successfully deleted."},
            status=status.HTTP_204_NO_CONTENT  # 204 for successful delete with no content
        )
