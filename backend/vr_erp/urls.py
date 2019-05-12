"""vr_erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from users.views import UserViewSet
from users.views import EmployeeViewSet
from users.views import CareerViewSet
from users.views import BehaviorSheetViewSet
from users.views import WorkScheduleViewSet
from users.views import WorkShiftViewSet
from products.views import ProductViewSet
from products.views import SaleViewSet
from products.views import StockViewSet
from core.views import ClientViewSet
from rest_framework.authtoken import views
from django.conf import settings
from products.views import AvailabilityView
from products.views import StockTransferView
from products.views import SaleTradeView
from products.views import ColorViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'careers', CareerViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'behavior_sheets', BehaviorSheetViewSet)
router.register(r'work_schedules', WorkScheduleViewSet)
router.register(r'work_shifts', WorkShiftViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(
        r'^api/auth/token/',
        views.obtain_auth_token, name='auth_token')
    ,
    url(
        r'^api/auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'^api/availability/$', AvailabilityView.as_view(), name='availability'),
    url(r'^api/stock/transfer/$', StockTransferView.as_view(), name='stock_transfer'),
    url(r'^api/sale/trade/$', SaleTradeView.as_view(), name='sale_trade'),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
