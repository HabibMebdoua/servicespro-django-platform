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
    link = models.URLField(null=True, blank=True)   # رابط الاستشارة
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'expert'})
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# طلب اشتراك من العميل للحصول على الاستشارة
class SubscriptionRequest(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='requests')
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consult_requests')
    status = models.CharField(max_length=20, choices=(('pending','pending'),('accepted','accepted'),('rejected','rejected')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} for Q#{self.question.id} by {self.client.username}"

# اشتراك فعلي بعد قبول الطلب
class Subscription(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='subscriptions')
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consult_subscriptions')
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription {self.id} Q#{self.question.id} - {self.client.username}"
