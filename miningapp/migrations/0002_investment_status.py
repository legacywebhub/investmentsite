# Generated by Django 3.2.2 on 2022-12-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miningapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved'), ('completed', 'Completed')], default='pending', max_length=60),
        ),
    ]
