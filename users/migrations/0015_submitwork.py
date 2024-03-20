# Generated by Django 4.2.10 on 2024-03-14 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_auth_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vidkey', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, max_length=400, null=True)),
                ('Quatation', models.DecimalField(decimal_places=2, max_digits=5)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]