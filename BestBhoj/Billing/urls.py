from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allorders', views.order_display, name='all_orders'),
    path('logout', views.log_out, name="logout"),
    path('takeorder', views.take_order, name='takeorder'),
    path('spec_order/<primary_key>', views.spec_order, name='specific_order'),
    path('ajax/phonesearch', views.ajax, name='AjaxPhoneSearch'),
    path('allcustomers', views.all_customers, name='all_customers'),
    path('dayrec', views.dayrec, name='dayrec'),
    path('custompage/<number>', views.custompage, name='custompage'),
    path('bill/<order_num>', views.genbill, name='genbill'),
    path('ajax/item_add', views.ajax_item_add, name='add_item')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
