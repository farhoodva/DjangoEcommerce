# Generated by Django 3.1.7 on 2021-04-24 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210423_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='payment_method',
        ),
    ]
