from django.shortcuts import render
from ecommerce.models import DeliveryPerson  # تأكد من استيراد نموذج DeliveryPerson

def display_workers(request):
    # جلب جميع عمال التوصيل
    workers = DeliveryPerson.objects.all()

    # تمرير عمال التوصيل إلى القالب
    return render(request, 'delivery/workers_list.html', {'workers': workers})
