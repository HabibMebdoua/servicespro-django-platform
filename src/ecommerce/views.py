from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, Product,CartItem, OrderItem, Order, DeliveryPerson
from collections import defaultdict
from django.core.mail import send_mail
from accounts.models import CustomUser
from django.http import JsonResponse
from epayement.models import Wallet
# عرض قائمة المتاجر
def store_list(request):
    # جلب الفلتر من الطلب (مثل الولاية)
    wilaya_filter = request.GET.get('wilaya')
    catigory_filter = request.GET.get('catigory')
    
    if wilaya_filter:
        stores = Store.objects.filter(wilaya=wilaya_filter)
    elif catigory_filter:
        stores = Store.objects.filter(catigory=catigory_filter)
    else:
        stores = Store.objects.all()
    
    wilayas = Store.WILAYAS_CHOICES  # جلب قائمة الولايات
    catigories = Store.CATIGORY_CHOICES
    return render(request, 'ecommerce/store_list.html', {'stores': stores, 'wilayas': wilayas , 'catigories':catigories})


# عرض تفاصيل متجر معين
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all()
    return render(request, 'ecommerce/store_detail.html', {'store': store, 'products': products})


# عرض قائمة المنتجات
def product_list(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/product_list.html', {'products': products})


# عرض تفاصيل منتج معين
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ecommerce/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'ecommerce/cart_detail.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.get(pk=item_id, user=request.user).delete()
    messages.success(request, 'تمت إزالة المنتج من السلة بنجاح.')
    return redirect('cart_detail')



@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

   
    if not cart_items:
        return redirect('cart_detail')

    store_items = defaultdict(list)
    for item in cart_items:
        store_items[item.product.store].append(item)

    for store, items in store_items.items():
        order = Order.objects.create(customer=request.user, store=store)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        
        # إرسال بريد إلكتروني للبائع
        send_mail(
            subject='طلب جديد في متجرك',
            message=f'مرحباً {store.owner.username}, لديك طلب جديد في متجرك "{store.name}". يرجى تسجيل الدخول إلى لوحة التحكم لمراجعة الطلب.',
            from_email='noreply@servicespro.com',
            recipient_list=[store.owner.email],
            fail_silently=False,
        )

    cart_items.delete()  # إفراغ السلة بعد الطلب
    messages.success(request, 'تمت معالجة الطلب بنجاح.')
    return render(request, 'ecommerce/order_success.html')




#### Client part
@login_required
def client_dashboard(request):
    # جلب جميع الطلبات الخاصة بالمستخدم الحالي
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'ecommerce/client_dashboard.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    # جلب الطلب بناءً على معرفه
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    # التحقق من حالة الطلب
    if order.status == 'pending':
        order.delete()
        messages.success(request, 'تم إلغاء الطلب بنجاح.')
    else:
        messages.error(request, 'لا يمكن إلغاء الطلب لأنه ليس في حالة "قيد المعالجة".')

    return redirect('client_dashboard')


##Seller part
@login_required
def seller_dashboard(request):
    # جلب المتجر الخاص بالمستخدم الحالي
    store = get_object_or_404(Store, owner=request.user)
    # جلب الطلبات الخاصة بالمتجر
    orders = Order.objects.filter(store=store).order_by('-created_at')
    # جلب المنتجات الخاصة بالمتجر
    products = store.products.all()
    # جلب عمال التوصيل الذين ينتمون لنفس الولاية
    delivery_persons = CustomUser.objects.filter(role='delivery', deliveryperson__wilaya=store.wilaya)
    return render(request, 'ecommerce/seller_dashboard.html', {'store': store, 'orders': orders, 'products': products, 'delivery_persons': delivery_persons})


from django.db import transaction

@login_required
def update_order_status(request, order_id):
    # جلب الطلب بناءً على معرفه
    order = get_object_or_404(Order, id=order_id, store__owner=request.user)

    # تحديث حالة الطلب
    if request.method == 'POST':
        new_status = request.POST.get('status')
        delivery_person_id = request.POST.get('delivery_person')

        if new_status:
            # إذا كانت الحالة الجديدة ليست "pending"، قم بتحويل الأموال
            if order.status == 'pending' and new_status != 'pending':
                try:
                    # الحصول على محفظة المشتري
                    buyer_wallet = Wallet.objects.filter(user=order.customer).first()
                    if not buyer_wallet:
                        messages.error(request, 'لا يمتلك الزبون محفظة. لا يمكن إتمام العملية.')
                        return redirect('seller_dashboard')

                    # الحصول على محفظة البائع
                    seller_wallet = Wallet.objects.filter(user=order.store.owner).first()
                    if not seller_wallet:
                        messages.error(request, 'لا يمتلك المتجر محفظة. يرجى إنشاء محفظة قبل إتمام العملية.')
                        return redirect('seller_dashboard')

                    # حساب إجمالي المبلغ لهذا الطلب
                    total_amount = sum(item.product.price * item.quantity for item in order.orderitem_set.all())

                    # التحقق من كفاية الرصيد
                    if buyer_wallet.balance < total_amount:
                        messages.error(request, 'رصيد الزبون غير كافٍ لإتمام العملية.')
                        return redirect('seller_dashboard')

                    # تحويل الأموال
                    with transaction.atomic():
                        buyer_wallet.balance -= total_amount
                        seller_wallet.balance += total_amount
                        buyer_wallet.save()
                        seller_wallet.save()

                        print(f'Seller balance {seller_wallet.balance}')
                        print(f'buyer balance {buyer_wallet.balance}')

                    messages.success(request, 'تم تحويل الأموال بنجاح.')

                except Exception as e:
                    messages.error(request, f'حدث خطأ أثناء تحويل الأموال: {str(e)}')
                    return redirect('seller_dashboard')

            # تحديث حالة الطلب
            order.status = new_status

        if delivery_person_id:
            delivery_person = CustomUser.objects.get(id=delivery_person_id)
            order.delivery_person = delivery_person

        order.save()
        messages.success(request, 'تم تحديث حالة الطلب بنجاح.')

    return redirect('seller_dashboard')

@login_required
def cancel_order_by_seller(request, order_id):
    # جلب الطلب بناءً على معرفه
    order = get_object_or_404(Order, id=order_id, store__owner=request.user)
    # إلغاء الطلب
    order.delete()
    messages.success(request, 'تم إلغاء الطلب بنجاح.')
    return redirect('seller_dashboard')


@login_required
def delivery_person_setup(request):
    # التحقق من نوع المستخدم
    if request.user.role != 'delivery':
        return redirect('index')  # إعادة التوجيه إذا لم يكن المستخدم عامل توصيل

    if request.method == 'POST':
        wilaya = request.POST.get('wilaya')
        vehicle_type = request.POST.get('vehicle_type')

        if wilaya and vehicle_type:
            # إنشاء أو تحديث بيانات عامل التوصيل
            DeliveryPerson.objects.update_or_create(
                user=request.user,
                defaults={
                    'wilaya': wilaya,
                    'vehicle_type': vehicle_type,
                }
            )
            messages.success(request, 'تم تسجيل بياناتك بنجاح.')
            return redirect('index')  # إعادة التوجيه إلى الصفحة الرئيسية بعد التسجيل

    # عرض نافذة التسجيل
    wilayas = Store.WILAYAS_CHOICES  # جلب قائمة الولايات
    return render(request, 'ecommerce/delivery_person_setup.html', {'wilayas': wilayas})

@login_required
def create_store(request):
    # التحقق من أن المستخدم ليس لديه متجر بالفعل
    if hasattr(request.user, 'store'):
        messages.error(request, 'لديك بالفعل متجر.')
        return redirect('seller_dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')
        wilaya = request.POST.get('wilaya')
        catigory = request.POST.get('catigory')

        if name and wilaya and catigory:
            # إنشاء متجر جديد
            Store.objects.create(
                owner=request.user,
                name=name,
                description=description,
                logo=logo,
                wilaya=wilaya,
                catigory=catigory
            )
            messages.success(request, 'تم إنشاء المتجر بنجاح.')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')

    # عرض نموذج إنشاء المتجر
    wilayas = Store.WILAYAS_CHOICES
    catigories = Store.CATIGORY_CHOICES
    return render(request, 'ecommerce/create_store.html', {'wilayas': wilayas , 'catigories':catigories})

@login_required
def create_product(request):
    # جلب المتجر الخاص بالمستخدم الحالي
    store = get_object_or_404(Store, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        if name and price and image:
            Product.objects.create(
                store=store,
                name=name,
                description=description,
                price=price,
                image=image,
            )
            messages.success(request, 'تم إنشاء المنتج بنجاح.')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')

    return render(request, 'ecommerce/create_product.html')


@login_required
def delete_product(request, product_id):
    # جلب المنتج بناءً على معرفه
    product = get_object_or_404(Product, id=product_id, store__owner=request.user)
    product.delete()
    messages.success(request, 'تم حذف المنتج بنجاح.')
    return redirect('seller_dashboard')

