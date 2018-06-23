from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<user_id>/allorders', views.order_display, name='all_orders'),
    path('logout', views.log_out, name="logout")
]