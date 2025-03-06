from django.urls import path

from products.apis import product_apis, tag_apis

urlpatterns = [
    path('products/',                       product_apis.ProductListApi.as_view()),
    path('products/create/',                product_apis.ProductCreateApi.as_view()),
    path('products/<str:slug>/',            product_apis.ProductDetailApi.as_view()),
    path('products/<str:slug>/update/',     product_apis.ProductUpdateApi.as_view()),
    path('products/<str:slug>/delete/',     product_apis.ProductDeleteApi.as_view()),

    path('tags/',                           tag_apis.TagListApi.as_view()),
    path('tags/create/',                    tag_apis.TagCreateApi.as_view()),
    path('tags/<str:slug>/',                tag_apis.TagDetailApi.as_view()),
    path('tags/<str:slug>/update/',         tag_apis.TagUpdateApi.as_view()),
    path('tags/<str:slug>/delete/',         tag_apis.TagDeleteApi.as_view()),
]
