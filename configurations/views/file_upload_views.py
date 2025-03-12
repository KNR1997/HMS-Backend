from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http import Http404

from configurations.models import FileAttachment


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_file(request):
    try:
        with transaction.atomic():
            # Get the uploaded files
            attachments = request.FILES.getlist('attachment[]')
            response_data = []

            # Process the files
            for attachment in attachments:
                file_attachment = FileAttachment.objects.create(
                    original=attachment,
                    thumbnail=attachment  # Adjust this if you generate thumbnails separately
                )

                # Save the file attachment
                file_attachment.save()

                # Construct the response data
                response_data.append({
                    'id': file_attachment.id,
                    'original': request.build_absolute_uri(file_attachment.original.url),
                    'thumbnail': request.build_absolute_uri(file_attachment.thumbnail.url),
                })

        # Return the response
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        # Return error response if an exception occurs during the creation process
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def remove_file(request, file_id):
    try:
        # Retrieve the file attachment by ID
        file_attachment = FileAttachment.objects.get(id=file_id)

        # Delete the file attachment
        file_attachment.delete()

        # Return a success response
        return Response({'message': 'File attachment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except FileAttachment.DoesNotExist:
        # Return a not found response if the file attachment does not exist
        raise Http404('File attachment not found.')
    except Exception as e:
        # Return an error response if an exception occurs
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
