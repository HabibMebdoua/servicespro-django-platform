from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson
from .forms import CourseForm, LessonForm
from django.contrib.auth.decorators import login_required


def course_list(request):
    # جلب جميع الدورات من قاعدة البيانات
    courses = Course.objects.all()

    # تطبيق الفلاتر بناءً على طلب المستخدم
    title_filter = request.GET.get('title', '')  # فلتر العنوان
    min_price = request.GET.get('min_price', '')  # الحد الأدنى للسعر
    max_price = request.GET.get('max_price', '')  # الحد الأقصى للسعر

    if title_filter:
        courses = courses.filter(title__icontains=title_filter)
    if min_price:
        courses = courses.filter(price__gte=min_price)
    if max_price:
        courses = courses.filter(price__lte=max_price)

    return render(request, 'courses_market/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    # الحصول على الدورة بناءً على معرفها
    course = get_object_or_404(Course, id=course_id)

    # جلب جميع الدروس المرتبطة بالدورة
    lessons = Lesson.objects.filter(course=course)

    return render(request, 'courses_market/course_detail.html', {'course': course, 'lessons': lessons})

def lesson_detail(request, lesson_id):
    # الحصول على الدرس بناءً على معرفه
    lesson = get_object_or_404(Lesson, id=lesson_id)

    return render(request, 'courses_market/lesson_detail.html', {'lesson': lesson})

@login_required
def teacher_dashboard(request):
    # جلب جميع الدورات الخاصة بالأستاذ الحالي
    courses = Course.objects.filter(instructor=request.user)

    # معالجة طلب إضافة دورة جديدة
    if request.method == 'POST' and 'add_course' in request.POST:
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.instructor = request.user  # تعيين الأستاذ الحالي كمالك الدورة
            course.save()
            return redirect('course_teacher_dashboard')  # العودة إلى لوحة التحكم بعد الإضافة

    # معالجة طلب تعديل الدورة
    elif request.method == 'POST' and 'edit_course_id' in request.POST:
        course_id = request.POST.get('edit_course_id')
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.course_date = request.POST.get('course_date', course.course_date)
        course.price = request.POST.get('price', course.price)
        if 'image' in request.FILES:
            course.image = request.FILES['image']
        course.save()
        return redirect('course_teacher_dashboard')  # العودة إلى لوحة التحكم بعد التعديل

    # معالجة طلب حذف الدورة
    elif request.method == 'POST' and 'delete_course_id' in request.POST:
        course_id = request.POST.get('delete_course_id')
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        course.delete()
        return redirect('course_teacher_dashboard')  # العودة إلى لوحة التحكم بعد الحذف

    # معالجة طلب إضافة درس جديد
    elif request.method == 'POST' and 'add_lesson' in request.POST:
        lesson_form = LessonForm(request.POST, request.FILES)
        if lesson_form.is_valid():
            lesson = lesson_form.save(commit=False)
            lesson.course = get_object_or_404(Course, id=request.POST.get('course_id'), instructor=request.user)
            lesson.save()
            return redirect('course_teacher_dashboard')  # العودة إلى لوحة التحكم بعد إضافة الدرس

    course_form = CourseForm()  # نموذج فارغ لإضافة دورة
    lesson_form = LessonForm()  # نموذج فارغ لإضافة درس
    return render(request, 'courses_market/teacher_dashboard.html', {
        'courses': courses,
        'course_form': course_form,
        'lesson_form': lesson_form
    })



