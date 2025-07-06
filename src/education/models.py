from django.db import models
from accounts.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    course_date = models.DateField()
    link = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title


class CourseRegistration(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {'مقبول' if self.is_accepted else 'غير مقبول'}"



