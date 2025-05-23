from django.urls import path
from . import views

urlpatterns = [
    path('bookworm/status/', views.get_bookworm_status, name='bookworm-status'),
    path('bookworm/feed/', views.feed_bookworm, name='bookworm-feed'),
]