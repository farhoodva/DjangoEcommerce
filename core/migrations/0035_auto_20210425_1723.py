# Generated by Django 3.1.7 on 2021-04-25 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_remove_shoppingcart_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategories',
            name='parent_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='core.categories'),
        ),
    ]
