# Generated by Django 2.0.6 on 2018-06-23 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0003_orders_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='amount',
            field=models.BooleanField(default=False),
        ),
    ]