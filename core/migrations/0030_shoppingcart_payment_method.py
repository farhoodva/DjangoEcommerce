# Generated by Django 3.1.7 on 2021-04-22 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20210415_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('stripe', 'stripe'), ('paypal', 'paypal')], max_length=10, null=True),
        ),
    ]
