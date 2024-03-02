# Generated by Django 4.2.10 on 2024-02-27 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_userprofile_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editor_requests', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editor_requests', to='users.post')),
            ],
        ),
    ]