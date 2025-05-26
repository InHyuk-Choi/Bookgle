from django.contrib import admin
from .models import Pheed, Comment, Bookworm  # 너가 만든 모델들

admin.site.register(Pheed)
admin.site.register(Comment)
admin.site.register(Bookworm)