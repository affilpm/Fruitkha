# Generated by Django 5.0.1 on 2024-05-18 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_alter_coupon_discount_percentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='Product',
            new_name='product',
        ),
    ]
