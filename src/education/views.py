from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import Course, CourseRegistration
from .forms import AddCourseForm

def course_list(request):
    # الحصول على جميع الدورات
    courses = Course.objects.all()

    # تطبيق الفلتر بناءً على طلب المستخدم
    title_filter = request.GET.get('title', '')  # فلتر العنوان
    min_price = request.GET.get('min_price', '')  # الحد الأدنى للسعر
    max_price = request.GET.get('max_price', '')  # الحد الأقصى للسعر

    if title_filter:
        courses = courses.filter(title__icontains=title_filter)
    if min_price:
        courses = courses.filter(price__gte=min_price)
    if max_price:
        courses = courses.filter(price__lte=max_price)

    return render(request, 'education/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    # الحصول على تفاصيل الدورة بناءً على معرفها
    course = Course.objects.get(id=course_id)

    return render(request, 'education/course_detail.html', {'course': course})

@login_required
def teacher_dashboard(request):
    # جلب جميع الكورسات الخاصة بالمعلم الحالي
    courses = Course.objects.filter(teacher=request.user)
    form = AddCourseForm()  # نموذج فارغ للتعديل
    return render(request, 'education/teacher_dashboard.html', {'courses': courses, 'form': form})

@login_required
def manage_course(request):
    # معالجة طلب تعديل الكورس
    if request.method == 'POST' and 'edit_course_id' in request.POST:
        course_id = request.POST.get('edit_course_id')
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        form = AddCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')  # العودة إلى لوحة التحكم بعد التعديل

    # معالجة طلب حذف الكورس
    elif request.method == 'POST' and 'delete_course_id' in request.POST:
        course_id = request.POST.get('delete_course_id')
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        course.delete()
        return redirect('teacher_dashboard')  # العودة إلى لوحة التحكم بعد الحذف

    return redirect('teacher_dashboard')  # العودة إلى لوحة التحكم في حالة عدم وجود طلب صحيح



def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  # تعيين المعلم الحالي كمالك الدورة
            course.save()
            return redirect('teacher_dashboard')  # العودة إلى لوحة التحكم بعد الإضافة
    else:
        form = AddCourseForm()

    return render(request, 'education/add_course.html', {'form': form})

@login_required
def register_course(request, course_id):
    # الحصول على الدورة بناءً على معرفها
    course = get_object_or_404(Course, id=course_id)

    # التحقق من أن التلميذ لم يسجل مسبقًا في الدورة
    existing_registration = CourseRegistration.objects.filter(student=request.user, course=course).exists()
    if existing_registration:
        messages.error(request, "لقد قمت بالتسجيل في هذه الدورة مسبقًا.")
        return redirect('course_detail', course_id=course_id)

    # إنشاء تسجيل جديد بحالة "غير مقبول"
    registration = CourseRegistration.objects.create(student=request.user, course=course, is_accepted=False)
    messages.success(request, "تم التسجيل في الدورة بنجاح. يرجى انتظار قبول المعلم.")
    return redirect('course_detail', course_id=course_id)

@login_required
def registered_students(request, course_id):
    # الحصول على الدورة بناءً على معرفها
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    # جلب جميع التسجيلات المرتبطة بالدورة
    registrations = CourseRegistration.objects.filter(course=course)

    return render(request, 'education/registered_students.html', {'course': course, 'registrations': registrations})

@login_required
def accept_student(request, registration_id):
    # الحصول على التسجيل بناءً على معرفه
    registration = get_object_or_404(CourseRegistration, id=registration_id, course__teacher=request.user)

    # تحديث حالة القبول
    registration.is_accepted = True
    registration.save()

    # إرسال بريد إلكتروني إلى التلميذ
    course_link = registration.course.link if registration.course.link else "#"
    subject = f"تم قبولك في الدورة: {registration.course.title}"
    message = f"""
    مرحبًا {registration.student.username},

    لقد تم قبولك في الدورة: {registration.course.title}.
    يمكنك الوصول إلى الدورة عبر الرابط التالي:
    {course_link}

    شكرًا لاختيارك خدماتنا.
    """
    recipient_email = registration.student.email
    send_mail(subject, message, 'admin@servicespro.com', [recipient_email])

    # عرض رسالة نجاح
    messages.success(request, f"تم قبول التلميذ {registration.student.username} في الدورة وتم إرسال بريد إلكتروني إليه.")
    return redirect('registered_students', course_id=registration.course.id)




