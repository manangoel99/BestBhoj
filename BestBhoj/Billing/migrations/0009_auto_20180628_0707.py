# Generated by Django 2.0.6 on 2018-06-28 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0008_auto_20180628_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orders',
            name='money_recieved',
            field=models.IntegerField(default=0),
        ),
    ]
