# Generated by Django 3.1.7 on 2021-04-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20210406_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['id'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='coupons',
            options={'verbose_name_plural': 'Coupons'},
        ),
        migrations.AlterModelOptions(
            name='subcategories',
            options={'ordering': ['id'], 'verbose_name_plural': 'SubCategories'},
        ),
        migrations.AlterField(
            model_name='coupons',
            name='amount',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coupons',
            name='percentage',
            field=models.BooleanField(default=False),
        ),
    ]