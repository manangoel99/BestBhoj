from django.db import models

# Create your models here.
class orders(models.Model):

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    #order = models.CharField(max_length=1000)
    quantity_60 = models.IntegerField(default=0)
    quantity_75 = models.IntegerField(default=0)
    quantity_100 = models.IntegerField(default=0)
    quantity_125 = models.IntegerField(default=0)
    quantity_150 = models.IntegerField(default=0)
    quantity_200 = models.IntegerField(default=0)
    remarks = models.CharField(max_length=1000)
    operator = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    amount = models.IntegerField()
    delivery_boy = models.CharField(max_length=100)
    money_recieved = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    def __str__ (self):
        return 'Order For ' + self.name 
