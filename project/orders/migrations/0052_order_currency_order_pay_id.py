# Generated by Django 5.0.1 on 2024-05-24 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0051_orderitem_refunded_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pay_id',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
