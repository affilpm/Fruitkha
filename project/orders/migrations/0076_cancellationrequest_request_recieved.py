# Generated by Django 5.0.6 on 2024-06-08 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0075_remove_cancellationrequest_review_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancellationrequest',
            name='request_recieved',
            field=models.BooleanField(default=False),
        ),
    ]
