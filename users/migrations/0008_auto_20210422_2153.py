# Generated by Django 3.1.7 on 2021-04-22 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210422_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='address_line1',
            new_name='address_line',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line2',
        ),
    ]
