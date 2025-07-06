from django import forms
from .models import Course

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'course_date', 'link', 'image', 'price']
        labels = {
            'title': 'عنوان الدورة',
            'description': 'وصف الدورة',
            'course_date': 'تاريخ الدورة',
            'link': 'رابط الدورة (اختياري)',
            'image': 'صورة الدورة (اختياري)',
            'price': 'سعر الدورة',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل عنوان الدورة...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل وصف الدورة...',
                'rows': 4
            }),
            'course_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'اختر تاريخ الدورة...'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رابط الدورة (اختياري)...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل سعر الدورة...'
            }),
        }