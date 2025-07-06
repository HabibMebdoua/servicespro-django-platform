from django.db import models
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'expert'})
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
