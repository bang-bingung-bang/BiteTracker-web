# Generated by Django 5.1.2 on 2024-10-27 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyBites', '0005_alter_mybites_user'),
        ('editbites', '0004_alter_product_options_alter_product_calorie_tag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybites',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='editbites.product'),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
