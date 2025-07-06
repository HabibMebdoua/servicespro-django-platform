from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Answer
from .forms import AnswerForm, QuestionForm

def question_list(request):
    # جلب جميع الاستشارات
    questions = Question.objects.all()

    # تطبيق الفلاتر بناءً على طلب المستخدم
    category_filter = request.GET.get('category', '')  # فلتر الفئة
    title_filter = request.GET.get('title', '')  # فلتر العنوان

    if category_filter:
        questions = questions.filter(category__name__icontains=category_filter)
    if title_filter:
        questions = questions.filter(title__icontains=title_filter)

    return render(request, 'consulting/question_list.html', {'questions': questions})

@login_required
def question_detail(request, question_id):
    # جلب الاستشارة بناءً على معرفها
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)

    # معالجة نشر جواب
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.expert = request.user  # تعيين المستخدم الحالي كخبير
            answer.save()
            messages.success(request, "تم نشر جوابك بنجاح.")
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()

    return render(request, 'consulting/question_detail.html', {'question': question, 'answers': answers, 'form': form})

@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # تعيين المستخدم الحالي كمالك للاستشارة
            question.save()
            messages.success(request, "تم نشر الاستشارة بنجاح.")
            return redirect('question_list')  # العودة إلى قائمة الاستشارات بعد النشر
    else:
        form = QuestionForm()
    return render(request, 'consulting/add_question.html', {'form': form})

