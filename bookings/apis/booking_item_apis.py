from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.services.booking_items_services import booking_item_delete


class BookingItemDeleteApi(APIView):
    @staticmethod
    def delete(request, booking_item_id: str):
        booking_item_delete(booking_item_id=booking_item_id)

        return Response(
            {"detail": "Booking Item successfully deleted."},
            status=status.HTTP_204_NO_CONTENT  # 204 for successful delete with no content
        )
