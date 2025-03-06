from django.http import Http404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from common import utils
from products.selectors import tag_list, tag_get_by_slug
from products.services import tag_services


class TagListApi(APIView):
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        slug = serializers.CharField()

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        tags = tag_list(filters=filters_serializer.validated_data)

        return utils.get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=tags,
            request=request,
        )


class TagCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        slug = serializers.CharField(required=True)
        details = serializers.CharField(required=False)
        image = serializers.IntegerField(required=False)
        icon = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        slug = serializers.CharField(required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tag = tag_services.tag_create(**serializer.validated_data)

        return Response(self.OutputSerializer(tag).data, status=status.HTTP_201_CREATED)


class TagUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        slug = serializers.CharField(required=True)
        description = serializers.CharField(required=True)
        price = serializers.IntegerField(required=True)
        status = serializers.CharField(required=True)
        product_type = serializers.CharField(required=True)

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tag = tag_get_by_slug(slug=slug)

        if tag is None:
            raise Http404

        product = tag_services.tag_update(tag=tag, **serializer.validated_data)

        return Response(TagCreateApi.OutputSerializer(product).data, status=status.HTTP_200_OK)


class TagDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.CharField()
        description = serializers.CharField()
        price = serializers.IntegerField()
        status = serializers.CharField()
        product_type = serializers.CharField()

    def get(self, request, slug):
        tag = tag_get_by_slug(slug=slug)

        return Response(self.OutputSerializer(tag).data, status=status.HTTP_200_OK)


class TagDeleteApi(APIView):
    @staticmethod
    def delete(slug):
        tag_services.tag_delete(tag_id=slug)
        return Response(status=status.HTTP_204_NO_CONTENT)

