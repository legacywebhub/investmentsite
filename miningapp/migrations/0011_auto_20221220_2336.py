# Generated by Django 3.2.2 on 2022-12-20 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miningapp', '0010_auto_20221218_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='profile',
            name='timezone',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]
