# Generated by Django 3.1.7 on 2021-04-02 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210402_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]