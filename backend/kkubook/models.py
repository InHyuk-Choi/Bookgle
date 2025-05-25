from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone


User = get_user_model()

LEVEL_EXPERIENCE_TABLE = {
    **{i: 300 + (i - 1) * 50 for i in range(1, 10)},
    **{i: 800 + (i - 10) * 100 for i in range(10, 20)},
    **{i: 1800 + (i - 20) * 150 for i in range(20, 30)},
    **{i: 3300 + (i - 30) * 200 for i in range(30, 40)},
    **{i: 5300 + (i - 40) * 250 for i in range(40, 50)},
    **{i: 7800 + (i - 50) * 350 for i in range(50, 60)},
    **{i: 11300 + (i - 60) * 500 for i in range(60, 100)},
    **{i: 31300 + (i - 100) * 1000 for i in range(100, 200)},
    **{i: 131300 + (i - 200) * 1500 for i in range(200, 400)},
    **{i: 431300 + (i - 400) * 2000 for i in range(400, 700)},
    **{i: 1031300 + (i - 700) * 2500 for i in range(700, 1001)},
}

class Bookworm(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bookworm')
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

    def experience_to_next_level(self):
        if self.level >= 1000:
            return 0
        return LEVEL_EXPERIENCE_TABLE.get(self.level, 999999999)
    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= self.experience_to_next_level():
            self.experience -= self.experience_to_next_level()
            self.level += 1
        self.save()


# 피드
class Pheed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='pheeds/', blank=True, null=True)
    like_users = models.ManyToManyField(User, related_name='liked_pheeds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 댓글
class Comment(models.Model):
    pheed = models.ForeignKey(Pheed, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





# 책 등록
class Book(models.Model):
    isbn = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    
class ReadingRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='readingrecord_set')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    pages = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(null=True, blank=True) 
    is_finished = models.BooleanField(default=False)

    def is_today_recorded(self):
        return self.last_updated == timezone.now().date()


# GPT + Wikipedia 기반으로 생성된 문제
class Question(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    choices = models.JSONField(default=list) # 객관식 문제
    correct_answer = models.CharField(max_length=255)
    # GPT가 생성한 문제인지 확인하기 위한 식별 필드 (나중에 GPT API로 문제 잘 생성되나 확인용)
    gpt_generated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
