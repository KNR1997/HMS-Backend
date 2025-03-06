from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializers import MeSerializer


@api_view(['GET'])
def me(request):
    try:
        # Get the currently authenticated user
        user = request.user
        serializer = MeSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
