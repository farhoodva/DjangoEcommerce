# Generated by Django 3.1.7 on 2021-04-01 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='img/Items'),
        ),
        migrations.AddField(
            model_name='item',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='img/Items'),
        ),
        migrations.AddField(
            model_name='item',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to='img/Items'),
        ),
    ]
