from django.urls import path, include
from . import views
from .views import bookworm_ranking

urlpatterns = [
    # 인증
    path('custom-login/', views.custom_login_view, name='custom-login'),
    path('custom-logout/', views.custom_logout_view, name='custom-logout'),
    path('token/refresh/', views.refresh_access_token_view, name='cookie-token-refresh'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),

    # 유저 정보
    path('me/', views.user_detail_view, name='user-detail'),

    # 포인트
    path('points/', views.get_user_points, name='get-user-points'),
    path('points/add/', views.add_user_points, name='add-user-points'),
    path('points/subtract/', views.subtract_user_points, name='subtract-user-points'),

    # 페이지 수
    path('pages/', views.get_user_pages, name='get-user-pages'),
    path('pages/set/', views.set_user_pages, name='set-user-pages'),

    # 먹이 구매
    path('food/purchase/', views.purchase_food, name='purchase-food'),

    # 팔로우
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),

    path('followers/username/<str:username>/', views.user_followers),
    path('following/username/<str:username>/', views.user_following),

    path('is-following/<int:user_id>/', views.is_following, name='is_following'),

    path('profile/upload/', views.upload_profile_image, name='upload-profile-image'),
    
    
    path('ranking/', bookworm_ranking),


    path('username/<str:username>/', views.user_profile_by_username),
]