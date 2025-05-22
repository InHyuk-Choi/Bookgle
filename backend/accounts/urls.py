from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    user_detail_view,
    get_user_points,
    add_user_points,
    subtract_user_points,
    get_user_pages,
    set_user_pages,
)

urlpatterns = [
    # 인증
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),

    # 유저 정보
    path('me/', user_detail_view, name='user-detail'),

    # 포인트
    path('points/', get_user_points, name='get-user-points'),
    path('points/add/', add_user_points, name='add-user-points'),
    path('points/subtract/', subtract_user_points, name='subtract-user-points'),

    # 페이지 수
    path('pages/', get_user_pages, name='get-user-pages'),
    path('pages/set/', set_user_pages, name='set-user-pages'),
]
