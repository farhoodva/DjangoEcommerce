# Generated by Django 3.1.7 on 2021-05-08 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_auto_20210505_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
