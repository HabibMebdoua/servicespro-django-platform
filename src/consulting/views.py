from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .models import Category, Question, Answer, SubscriptionRequest, Subscription
from accounts.models import CustomUser
from .forms import AnswerForm, QuestionForm

def question_list(request):
    # جلب جميع الاستشارات
    categories = Category.objects.all()
    qs = Question.objects.all().order_by('-created_at')

    # تطبيق الفلاتر بناءً على طلب المستخدم
    category_filter = request.GET.get('category', '')  # فلتر الفئة
    title_filter = request.GET.get('title', '')  # فلتر العنوان

    if category_filter:
        qs = qs.filter(category__name__icontains=category_filter)
    if title_filter:
        qs = qs.filter(title__icontains=title_filter)

    return render(request, 'consulting/question_list.html', {'questions': qs, 'categories': categories})

def question_detail(request, question_id):
    # جلب الاستشارة بناءً على معرفها
    q = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=q)

    # تحقق هل العميل لديه طلب / اشتراك
    existing_request = None
    existing_subscription = None
    if request.user.is_authenticated:
        existing_request = SubscriptionRequest.objects.filter(question=q, client=request.user).order_by('-created_at').first()
        existing_subscription = Subscription.objects.filter(question=q, client=request.user).first()

    # معالجة نشر جواب
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = q
            answer.expert = request.user  # تعيين المستخدم الحالي كخبير
            answer.save()
            messages.success(request, "تم نشر جوابك بنجاح.")
            return redirect('question_detail', question_id=q.id)
    else:
        form = AnswerForm()

    return render(request, 'consulting/question_detail.html', {
        'question': q,
        'answers': answers,
        'form': form,
        'existing_request': existing_request,
        'existing_subscription': existing_subscription,
    })

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

@login_required
def request_subscription(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    if request.user == q.user:
        messages.error(request, 'لا يمكنك طلب اشتراك لاستشارتك الخاصة.')
        return redirect('question_detail', question_id=question_id)

    if SubscriptionRequest.objects.filter(question=q, client=request.user, status='pending').exists():
        messages.info(request, 'لديك طلب معلق مسبقاً لهذه الاستشارة.')
        return redirect('question_detail', question_id=question_id)

    SubscriptionRequest.objects.create(question=q, client=request.user)
    messages.success(request, 'تم إرسال طلب الاشتراك. سيتواصل معك صاحب الاستشارة بعد المراجعة.')
    return redirect('question_detail', question_id=question_id)

@login_required
def expert_requests(request):
    # يعرض طلبات كل الأسئلة التي يملكها المستخدم
    reqs = SubscriptionRequest.objects.filter(question__user=request.user).order_by('-created_at')
    return render(request, 'consulting/expert_requests.html', {'requests': reqs})

@login_required
def handle_request(request, req_id):
    req = get_object_or_404(SubscriptionRequest, id=req_id, question__user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept' and req.status == 'pending':
            with transaction.atomic():
                req.status = 'accepted'
                req.save()
                Subscription.objects.create(question=req.question, client=req.client)
            # إرسال إيميل للعميل مع رابط الاستشارة
            if req.question.link and req.client.email:
                subject = 'تم قبول طلب الاشتراك في الاستشارة'
                message = f'مرحباً {req.client.username},\n\nتم قبول طلبك في الاستشارة "{req.question.title}".\nيمكنك الوصول إلى رابط الاستشارة هنا:\n{req.question.link}\n\nمع تحياتنا.'
                send_mail(subject, message, getattr(settings, 'DEFAULT_FROM_EMAIL', None), [req.client.email], fail_silently=True)
            messages.success(request, 'تم قبول الطلب وإرسال الرابط للعميل.')
        elif action == 'reject' and req.status == 'pending':
            req.status = 'rejected'
            req.save()
            messages.info(request, 'تم رفض الطلب.')
    return redirect('expert_requests')

