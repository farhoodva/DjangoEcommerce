# Generated by Django 3.1.7 on 2021-05-08 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_item_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='thumbnail',
        ),
    ]
