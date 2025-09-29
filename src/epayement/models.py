import uuid
from django.db import models
from accounts.models import CustomUser

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveBigIntegerField(default=1000)
    code = models.CharField(max_length=36, unique=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8]  # رمز قصير للتجربة
        super().save(*args, **kwargs)  # الحفظ يتم دائماً وليس فقط عند إنشاء الكود

    def __str__(self):
        return f"{self.user.username} - {self.balance} DZD"