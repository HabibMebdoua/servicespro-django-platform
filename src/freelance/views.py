from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # استيراد مكتبة الرسائل
from django.contrib.auth.decorators import login_required
from .models import Service, Order
from .forms import OrderForm, ServiceForm
from django.core.mail import send_mail  # استيراد مكتبة إرسال البريد الإلكتروني

def available_services(request):
    # جلب جميع الخدمات المتاحة
    services = Service.objects.all()

    # تطبيق الفلاتر بناءً على طلب المستخدم
    title_filter = request.GET.get('title', '')  # فلتر العنوان
    min_price = request.GET.get('min_price', '')  # الحد الأدنى للسعر
    max_price = request.GET.get('max_price', '')  # الحد الأقصى للسعر

    if title_filter:
        services = services.filter(title__icontains=title_filter)
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)

    return render(request, 'freelance/available_services.html', {'services': services})

def request_service(request, service_id):
    # جلب الخدمة بناءً على معرفها
    service = get_object_or_404(Service, id=service_id)

    # تسجيل الطلب مباشرة عند الضغط على الزر
    if request.method == 'POST':
        Order.objects.create(
            service=service,
            client=request.user,
            status='pending'  # الحالة الافتراضية للطلب
        )
        messages.success(request, f"تم إرسال طلبك بنجاح للخدمة: {service.title}")  # إضافة رسالة نجاح
        return redirect('available_services')  # العودة إلى صفحة الخدمات بعد تسجيل الطلب

    return render(request, 'freelance/request_service.html', {'service': service})

@login_required
def freelancer_dashboard(request):
    # جلب الطلبات المرتبطة بالخدمات الخاصة بالفريلانسر
    orders = Order.objects.filter(service__user=request.user)

    # جلب الخدمات الخاصة بالفريلانسر
    services = Service.objects.filter(user=request.user)

    # معالجة قبول أو رفض الطلب
    if request.method == 'POST' and 'order_id' in request.POST:
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')  # "accept" أو "reject"
        order = get_object_or_404(Order, id=order_id, service__user=request.user)
        if action == 'accept':
            order.status = 'delivered'
            order.save()
            messages.success(request, f"تم قبول الطلب رقم {order.id}.")

            # إرسال بريد إلكتروني إلى العميل
            send_mail(
                subject=f"تم قبول طلبك للخدمة: {order.service.title}",
                message=f"مرحبًا {order.client.username},\n\nتم قبول طلبك للخدمة: {order.service.title}.\n\nشكرًا لاستخدامك منصتنا!",
                from_email='no-reply@services_pro.com',
                recipient_list=[order.client.email],
                fail_silently=False,
            )
        elif action == 'reject':
            order.status = 'rejected'
            order.save()
            messages.warning(request, f"تم رفض الطلب رقم {order.id}.")
        return redirect('freelancer_dashboard')

    # معالجة تعديل أو حذف الخدمة
    elif request.method == 'POST' and 'service_id' in request.POST:
        service_id = request.POST.get('service_id')
        action = request.POST.get('action')  # "edit", "delete", أو "toggle_availability"
        service = get_object_or_404(Service, id=service_id, user=request.user)
        if action == 'delete':
            service.delete()
            messages.success(request, f"تم حذف الخدمة: {service.title}.")
        elif action == 'toggle_availability':
            service.is_available = not service.is_available
            service.save()
            status = "متاحة" if service.is_available else "غير متاحة"
            messages.success(request, f"تم تغيير حالة الخدمة إلى: {status}.")
        elif action == 'edit':
            service.title = request.POST.get('title', service.title)
            service.description = request.POST.get('description', service.description)
            service.price = request.POST.get('price', service.price)
            if 'image' in request.FILES:
                service.image = request.FILES['image']
            service.save()
            messages.success(request, f"تم تعديل الخدمة: {service.title}.")
        return redirect('freelancer_dashboard')

    return render(request, 'freelance/freelancer_dashboard.html', {'orders': orders, 'services': services})


@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user  # تعيين المستخدم الحالي كمالك للخدمة
            service.save()
            messages.success(request, f"تم إضافة الخدمة بنجاح: {service.title}.")
            return redirect('freelancer_dashboard')  # العودة إلى لوحة التحكم بعد الإضافة
        else:
            messages.error(request, "حدث خطأ أثناء إضافة الخدمة. يرجى التحقق من البيانات.")
    else:
        form = ServiceForm()
    return render(request, 'freelance/add_service.html', {'form': form})

@login_required
def client_dashboard(request):
    # جلب الطلبات الخاصة بالعميل الحالي
    orders = Order.objects.filter(client=request.user)

    # معالجة رفض أو إنهاء الطلب
    if request.method == 'POST' and 'order_id' in request.POST:
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id, client=request.user)
        if order.status != 'delivered':  # يمكن رفض الطلب فقط إذا لم يكن مقبولاً
            order.delete()  # حذف الطلب من قاعدة البيانات
            messages.success(request, f"تم رفض الطلب رقم {order_id} وتم حذفه.")
        else:
            messages.error(request, f"لا يمكن رفض الطلب رقم {order_id} لأنه قد تم قبوله بالفعل.")
        return redirect('client_dashboard')

    return render(request, 'freelance/client_dashboard.html', {'orders': orders})




