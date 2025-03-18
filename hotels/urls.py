from django.urls import path

from hotels.apis import room_apis, room_category_apis, hotel_apis

urlpatterns = [
    path('rooms/',                                          room_apis.RoomListApi.as_view()),
    path('rooms/create',                                    room_apis.RoomCreateApi.as_view()),
    path('rooms/<slug:room_number>',                        room_apis.RoomDetailApi.as_view()),
    path('rooms/<str:room_number>/update',                  room_apis.RoomUpdateApi.as_view()),
    path('rooms/<str:room_id>/delete',                      room_apis.RoomDeleteApi.as_view()),

    path('room-categories/',                                room_category_apis.RoomCategoryListApi.as_view()),
    path('room-categories/create',                          room_category_apis.RoomCategoryCreateApi.as_view()),
    path('room-categories/<slug:slug>',                     room_category_apis.AdminRoomCategoryDetailApi.as_view()),
    path('room-categories/<str:slug>/update',               room_category_apis.RoomCategoryUpdateApi.as_view()),
    path('room-categories/<str:room_category_id>/delete',   room_category_apis.RoomCategoryDeleteApi.as_view()),

    path('web/room-categories/<slug:slug>',                 room_category_apis.PublicRoomCategoryDetailApi.as_view()),

    path('hotels',                                          hotel_apis.HotelDetailApi.as_view()),
    path('hotel/update',                                    hotel_apis.HotelUpdateApi.as_view()),

]