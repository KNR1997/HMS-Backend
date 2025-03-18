from django.db import transaction
from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.selectors import hotel_get
from hotels.services.hotel_services import hotel_update


class HotelDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        location = serializers.CharField()
        description = serializers.CharField()
        rating = serializers.CharField()
        amenities = serializers.CharField()
        image = serializers.CharField()

    def get(self, request):
        hotel = hotel_get()

        if hotel is None:
            raise Http404

        data = self.OutputSerializer(hotel).data

        return Response(data)


class HotelUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        location = serializers.CharField()
        description = serializers.CharField()


    @transaction.atomic
    def put(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hotel = hotel_get()

        if hotel is None:
            raise Http404

        hotel = hotel_update(hotel=hotel, data=serializer.validated_data)

        # Note: This shows a possible reusability for serializers between APIs
        # Usually, this is how we approach things, when building APIs at first
        # But at the very moment when we need to make a change to the output,
        # that's specific to this API, we'll introduce a separate OutputSerializer just for this API
        data = HotelDetailApi.OutputSerializer(hotel).data

        return Response(data)

