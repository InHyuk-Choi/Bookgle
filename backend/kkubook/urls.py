from django.urls import path
from . import views

urlpatterns = [
    # Bookworm
    path('bookworm/status/', views.get_bookworm_status, name='bookworm-status'),
    path('bookworm/feed/', views.feed_bookworm, name='bookworm-feed'),

    # Pheeds
    path('pheeds/', views.list_create_pheeds, name='pheed-list-create'),
    path('pheeds/<int:pheed_id>/', views.update_delete_pheed, name='pheed-detail'),
    path('pheeds/<int:pheed_id>/like/', views.toggle_like_pheed, name='pheed-like'),
    path('pheeds/me/', views.my_pheeds, name='my-pheeds'),
    path('pheeds/user/<str:username>/', views.user_pheeds_by_username),

    # Comments
    path('pheeds/<int:pheed_id>/comments/', views.list_create_comments, name='comment-list-create'),
    path('comments/<int:comment_id>/', views.update_delete_comment, name='comment-detail'),

    # Pages
    path('pages/set/', views.set_pages),

    # Books
    path('books/search/', views.search_books, name='search-books'),
    path('books/register/', views.register_book, name='register-book'),
    path('books/finish/', views.finish_current_book, name='finish-book'),
    path('books/recommend/', views.recommend_books, name='recommend-books'),
    path('books/<str:isbn>/', views.get_book_detail, name='book-detail'),

    # Reviews
    path('books/<str:isbn>/reviews/', views.list_create_reviews, name='review-list-create'),
    path('reviews/<int:review_id>/', views.update_delete_review, name='review-detail'),

    # Quiz
    path('questions/generate/', views.generate_quiz_view, name='generate-quiz'),
    path('questions/quiz-complete/', views.quiz_complete_view),
]