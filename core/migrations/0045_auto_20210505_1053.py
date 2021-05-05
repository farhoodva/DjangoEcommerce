# Generated by Django 3.1.7 on 2021-05-05 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0044_auto_20210504_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='review',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]