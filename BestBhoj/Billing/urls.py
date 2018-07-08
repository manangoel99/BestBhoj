from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allorders', views.order_display, name='all_orders'),
    path('logout', views.log_out, name="logout"),
    path('takeorder', views.take_order, name='takeorder'),
    path('spec_order/<primary_key>', views.spec_order, name='specific_order'),
    path('ajax/phonesearch', views.ajax, name='AjaxPhoneSearch'),
    path('allcustomers', views.all_customers, name='all_customers'),
    path('dayrec', views.dayrec, name='dayrec')
]