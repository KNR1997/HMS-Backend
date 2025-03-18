from django.urls import path

from accounts.apis import user_apis, admin_apis
from accounts.views.login_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView, RegisterView,
)

urlpatterns = [
    path('register',        RegisterView.as_view(), name='register'),
    path('token',           CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/',    CustomTokenRefreshView.as_view()),
    path('jwt/verify/',     CustomTokenVerifyView.as_view()),
    path('logout',          LogoutView.as_view()),

    path('me/',             user_apis.UserDetailApi.as_view()),
    path('users/',          user_apis.UserListApi.as_view()),

    path('admin/list',      admin_apis.AdminListApi.as_view()),

]
