# Generated by Django 4.2.10 on 2024-03-14 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_submitwork'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitwork',
            name='Quatation',
            field=models.IntegerField(),
        ),
    ]
