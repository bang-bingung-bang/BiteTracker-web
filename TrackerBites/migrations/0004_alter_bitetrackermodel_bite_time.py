# Generated by Django 5.1.2 on 2024-10-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrackerBites', '0003_alter_bitetrackermodel_bite_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitetrackermodel',
            name='bite_time',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], max_length=10),
        ),
    ]