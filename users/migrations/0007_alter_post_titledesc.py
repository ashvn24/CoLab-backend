# Generated by Django 4.2.10 on 2024-02-22 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_post_titledesc_alter_post_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='titleDesc',
            field=models.CharField(max_length=400, null=True),
        ),
    ]