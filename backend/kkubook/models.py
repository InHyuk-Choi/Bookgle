from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

LEVEL_EXPERIENCE_TABLE = {
    **{i: 300 + (i - 1) * 50 for i in range(1, 10)},
    **{i: 800 + (i - 10) * 100 for i in range(10, 20)},
    **{i: 1800 + (i - 20) * 150 for i in range(20, 30)},
    **{i: 3300 + (i - 30) * 200 for i in range(30, 40)},
    **{i: 5300 + (i - 40) * 250 for i in range(40, 50)},
    **{i: 7800 + (i - 50) * 350 for i in range(50, 60)},
    **{i: 11300 + (i - 60) * 500 for i in range(60, 71)},
}

class Bookworm(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bookworm')
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

    def experience_to_next_level(self):
        return LEVEL_EXPERIENCE_TABLE.get(self.level, 999999999) # 9999..는 레벨이 한도를 초과했을 때를 대비한 보호장치

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

