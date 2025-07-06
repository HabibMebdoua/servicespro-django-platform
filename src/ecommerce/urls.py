from django.urls import path
from . import views

urlpatterns = [
    # عرض قائمة المتاجر
    path('stores/', views.store_list, name='store_list'),
    
    # عرض تفاصيل متجر معين
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    
    # عرض قائمة المنتجات
    path('products/', views.product_list, name='product_list'),
    
    # عرض تفاصيل منتج معين
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # إضافة منتج إلى السلة
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # عرض تفاصيل السلة
    path('cart/', views.cart_detail, name='cart_detail'),
    
    # إزالة منتج من السلة
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # إنشاء طلب جديد
    path('cart/place-order/', views.place_order, name='place_order'),
    
    # لوحة تحكم العميل
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    
    # إلغاء الطلب
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # لوحة تحكم المتجر
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),

    # إنشاء منتج جديد
    path('create-product/', views.create_product, name='create_product'),

    # حذف منتج
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    # تحديث حالة الطلب
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),

    # إلغاء الطلب بواسطة صاحب المتجر
    path('cancel-order-by-seller/<int:order_id>/', views.cancel_order_by_seller, name='cancel_order_by_seller'),

    # تسجيل بيانات عامل التوصيل
    path('delivery-person-setup/', views.delivery_person_setup, name='delivery_person_setup'),
    path('create-store/', views.create_store, name='create_store'),
]