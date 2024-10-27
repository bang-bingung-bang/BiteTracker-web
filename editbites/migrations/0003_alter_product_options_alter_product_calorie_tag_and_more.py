# Generated by Django 5.1 on 2024-10-25 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editbites', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={},
        ),
        migrations.AlterField(
            model_name='product',
            name='calorie_tag',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='sugar_tag',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='vegan_tag',
            field=models.CharField(choices=[('VEGAN', 'Vegan'), ('NON_VEGAN', 'Non-Vegan')], max_length=10),
        ),
    ]