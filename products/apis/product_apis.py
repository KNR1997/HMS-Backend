from django.http import Http404
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from common import utils
from products.selectors import product_list, product_get_by_slug
from products.services import product_services


class ProductListApi(APIView):
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

        products = product_list(filters=filters_serializer.validated_data)

        return utils.get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=products,
            request=request,
        )


class ProductCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        slug = serializers.CharField(required=True)
        description = serializers.CharField(required=False)
        price = serializers.IntegerField(required=True)
        status = serializers.CharField(required=True)
        product_type = serializers.CharField(required=True)

    class OutputSerializer(serializers.Serializer):
        slug = serializers.CharField(required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = product_services.product_create(**serializer.validated_data)

        return Response(self.OutputSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductUpdateApi(APIView):
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

        product = product_get_by_slug(slug=slug)

        if product is None:
            raise Http404

        product = product_services.product_update(product=product, **serializer.validated_data)

        return Response(ProductCreateApi.OutputSerializer(product).data, status=status.HTTP_200_OK)


class ProductDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.CharField()
        description = serializers.CharField()
        price = serializers.IntegerField()
        status = serializers.CharField()
        product_type = serializers.CharField()

    def get(self, request, slug):
        product = product_get_by_slug(slug=slug)

        return Response(self.OutputSerializer(product).data, status=status.HTTP_200_OK)


class ProductDeleteApi(APIView):
    @staticmethod
    def delete(slug):
        product_services.product_delete(product_id=slug)
        return Response(status=status.HTTP_204_NO_CONTENT)
