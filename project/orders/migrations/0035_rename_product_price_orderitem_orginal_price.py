# Generated by Django 5.0.1 on 2024-05-21 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0034_remove_order_original_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product_price',
            new_name='orginal_price',
        ),
    ]
