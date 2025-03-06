from rest_framework import serializers
from rest_framework.views import APIView

from common import utils
from products.selectors import category_list


class CategoryListApi(APIView):
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

        categories = category_list(filters=filters_serializer.validated_data)

        return utils.get_paginated_response(
            serializer_class=self.OutputSerializer,
            queryset=categories,
            request=request,
        )
