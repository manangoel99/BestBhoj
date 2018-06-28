from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allorders', views.order_display, name='all_orders'),
    path('logout', views.log_out, name="logout"),
    path('takeorder', views.take_order, name='takeorder')
]