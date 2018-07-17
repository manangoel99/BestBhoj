from django.contrib import admin
from .models import orders, customers, menu
# Register your models here.

admin.site.register(orders)
admin.site.register(customers)
admin.site.register(menu)