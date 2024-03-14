# Generated by Django 4.2.10 on 2024-03-14 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_submitwork_quatation'),
        ('Notification', '0003_alter_notification_obj'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='work',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_notification', to='users.submitwork'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_notification', to='users.editorrequest'),
        ),
    ]
