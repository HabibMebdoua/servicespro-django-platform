from django import forms
from .models import Service, Order

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'image']  # إضافة حقل الصورة
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الخدمة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'وصف الخدمة', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'السعر'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),  # تخصيص حقل الصورة
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service', 'status']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }