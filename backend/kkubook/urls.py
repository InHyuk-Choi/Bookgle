from django.urls import path
from . import views

urlpatterns = [
    # Bookworm
    path('bookworm/status/', views.get_bookworm_status, name='bookworm-status'),
    path('bookworm/feed/', views.feed_bookworm, name='bookworm-feed'),

    # Pheed (GET + POST)
    path('pheeds/', views.list_create_pheeds, name='pheed-list-create'),

    # Pheed (PUT + DELETE)
    path('pheeds/<int:pheed_id>/', views.update_delete_pheed, name='pheed-detail'),

    # Like
    path('pheeds/<int:pheed_id>/like/', views.toggle_like_pheed, name='pheed-like'),

    # Comment (GET + POST)
    path('pheeds/<int:pheed_id>/comments/', views.list_create_comments, name='comment-list-create'),

    # Comment (PUT + DELETE)
    path('comments/<int:comment_id>/', views.update_delete_comment, name='comment-detail'),
    
    path('pheeds/me/', views.my_pheeds, name='my-pheeds'),  
    path('pheeds/user/<str:username>/', views.user_pheeds_by_username),
    path('pages/set/', views.set_pages),
    path('books/search/', views.search_books, name='search-books'),
    path('books/register/', views.register_book, name='register-book'),

    path('books/finish/', views.finish_current_book, name='finish-book'),
    path('questions/generate/', views.generate_quiz_view, name='generate-quiz'),
    path('books/quiz-complete/', views.quiz_complete_view),
]