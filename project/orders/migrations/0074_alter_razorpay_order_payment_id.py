# Generated by Django 5.0.1 on 2024-06-01 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0073_alter_razorpay_order_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='razorpay_order',
            name='payment_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
