from django.db import models
from accounts.models import CustomUser

class Service(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class Order(models.Model):
    client = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('rejected', 'Rejected')])
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order {self.id} for {self.service.title} by {self.client.username}"
