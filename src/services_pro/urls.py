
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('education/' , include('education.urls')),
    path('courses/', include('courses_market.urls')),
    path('freelance/', include('freelance.urls')),
    path('consulting/', include('consulting.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('delivery/', include('delivery.urls')),
    path('epayement/' , include('epayement.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
