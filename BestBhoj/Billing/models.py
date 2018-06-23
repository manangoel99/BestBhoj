from django.db import models

# Create your models here.
class orders(models.Model):

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    order = models.CharField(max_length=1000)
    remarks = models.CharField(max_length=1000)
    operator = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    amount = models.IntegerField()

    def __str__ (self):
        return 'Order For ' + self.name 