# Generated by Django 5.0.1 on 2024-06-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_tag_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, related_name='related_to', to='home.product'),
        ),
    ]
