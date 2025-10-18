from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    ROLE_CHOICES = (
        ('member', 'مستخدم'),
        ('freelancer', 'freelancer'),
        ('teacher', 'مدرس'),
        ('delivery', 'عامل توصيل'),
        ('courses_instructor', 'إستاذ دورات'),
        ('seller', 'بائع'),
        ('consulter', 'مقدم إستشارات'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name="نبذة عن المستخدم")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="العنوان")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="صورة الملف الشخصي")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="تاريخ الميلاد")

    def __str__(self):
        return f"Profile of {self.user.username}"
