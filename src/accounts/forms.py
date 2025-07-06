from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2', 'role')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'address', 'profile_picture', 'date_of_birth']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'اكتب نبذة عنك...',
                'rows': 4
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل عنوانك...'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'bio': 'نبذة عن المستخدم',
            'address': 'العنوان',
            'profile_picture': 'صورة الملف الشخصي',
            'date_of_birth': 'تاريخ الميلاد',
        }
