# Generated by Django 4.2.10 on 2024-02-27 20:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_editorrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='editorrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]