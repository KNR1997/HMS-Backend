from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def make_mock_object(**kwargs):
    return type("", (object,), kwargs)


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def assert_settings(required_settings, error_message_prefix=""):
    """
    Checks if each item from `required_settings` is present in Django settings
    """
    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_setting):
            not_present.append(required_setting)
            continue

        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."

        stringified_not_present = ", ".join(not_present)

        raise ImproperlyConfigured(f"{error_message_prefix} Could not find: {stringified_not_present}")

    return values


def get_paginated_response(*, serializer_class, queryset, request):
    query_params = request.query_params
    limit = int(query_params.get("limit", 10))
    page = int(query_params.get("page", 1))
    order_by = query_params.get("orderBy", "id")
    sorted_by = query_params.get("sortedBy", "asc")

    # Apply order_by and sorted_by
    if order_by is not None:
        if sorted_by == "asc":
            order_by = f"{order_by}"
        else:
            order_by = f"-{order_by}"
        queryset = queryset.order_by(order_by)

    # Paginate the results
    paginator = Paginator(queryset, limit)
    current_page = paginator.page(page)

    # Serialize the data
    serializer = serializer_class(current_page.object_list, many=True)

    # Prepare pagination info
    pagination_info = {
        'total': paginator.count,
        'perPage': limit,
        'currentPage': int(page),
        'lastPage': paginator.num_pages,
    }

    return Response({
        'data': serializer.data, **pagination_info}, status=status.HTTP_200_OK)


def parse_search_query(search_query: str) -> dict:
    """
    Parse a `search` query string in the format `key1:value1;key2:value2`.

    Args:
        search_query (str): The `search` query string.

    Returns:
        dict: A dictionary of parsed filters.
    """
    filters = {}
    if search_query:
        search_filters = search_query.split(';')
        for filter_item in search_filters:
            try:
                field, value = filter_item.split(':', 1)
                filters[field] = value
            except ValueError:
                # Skip malformed filters
                continue
    return filters
