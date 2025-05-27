from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

urlpatterns = [
    path('', lambda request: HttpResponse("✅ Kakao 로그인 성공! 여기가 홈이야!")),  # ← 이거 한 줄
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/kkubook/', include('kkubook.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
