from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Wallet

@login_required
def wallet_details(request):
    wallet = get_object_or_404(Wallet , user=request.user)

    context={
        'wallet' : wallet
    }

    return render(request , 'epayement/wallet_details.html' , context)

@login_required
def deposit_funds(request):
    if request.method == 'POST':
        wallet_code = request.POST.get('wallet_code')
        amount = request.POST.get('amount')

        # التحقق من صحة البيانات المدخلة
        if not wallet_code or not amount:
            messages.error(request, 'يرجى إدخال رمز المحفظة والمبلغ.')
            return redirect('deposit_funds')

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'المبلغ يجب أن يكون أكبر من 0.')
                return redirect('deposit_funds')
        except ValueError:
            messages.error(request, 'يرجى إدخال مبلغ صالح.')
            return redirect('deposit_funds')

        # البحث عن المحفظة المستهدفة
        target_wallet = Wallet.objects.filter(code=wallet_code).first()
        if not target_wallet:
            messages.error(request, 'رمز المحفظة غير صحيح.')
            return redirect('deposit_funds')

        # التحقق من وجود رصيد كافٍ في محفظة المستخدم الحالي
        user_wallet = Wallet.objects.filter(user=request.user).first()
        if not user_wallet:
            messages.error(request, 'لا تمتلك محفظة. يرجى إنشاء محفظة أولاً.')
            return redirect('deposit_funds')

        if user_wallet.balance < amount:
            messages.error(request, 'رصيدك غير كافٍ لإتمام العملية.')
            return redirect('deposit_funds')

        # تنفيذ عملية الإيداع
        with transaction.atomic():
            user_wallet.balance -= amount
            target_wallet.balance += amount
            user_wallet.save()
            target_wallet.save()

        messages.success(request, f'تم إيداع {amount} دج بنجاح في المحفظة ذات الرمز {wallet_code}.')
        return redirect('wallet_details')

    return render(request, 'epayement/deposit.html')

