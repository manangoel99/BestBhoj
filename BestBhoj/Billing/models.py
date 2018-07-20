from django.db import models

# Create your models here.
class orders(models.Model):

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    order = models.CharField(max_length = 10000)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    operator = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    amount = models.IntegerField()
    delivery_boy = models.CharField(max_length=100, null=True, blank=True)
    money_received = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    delivery_status = models.BooleanField(default=False)
    money_receive_date = models.DateField(null=True, blank=True)

    def __str__ (self):
        return 'Order For ' + self.name 

class customers(models.Model):
    number = models.CharField(max_length=15)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return 'Customer : ' + self.number + ' ' + str(self.balance)

class menu(models.Model):
    item = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk) + ' ' + self.item + ' : ' + str(self.price)
