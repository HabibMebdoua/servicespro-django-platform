from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'رابط الاستشارة (اختياري)'
    }))

    class Meta:
        model = Question
        fields = ['category', 'title', 'content', 'link']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الاستشارة'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'محتوى الاستشارة', 'rows': 5}),
        }

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if link:
            # يمكن إضافة تحقق إضافي هنا إن لزم (مثلاً السماح بروتوكولات محددة)
            return link
        return link

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'اكتب جوابك هنا...', 'rows': 5}),
        }