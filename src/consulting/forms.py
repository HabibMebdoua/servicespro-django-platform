from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'title', 'content']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الاستشارة'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'محتوى الاستشارة', 'rows': 5}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'اكتب جوابك هنا...', 'rows': 5}),
        }