# Generated by Django 5.1.2 on 2024-10-26 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrackerBites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitetrackermodel',
            name='bite_date',
            field=models.DateField(null=True),
        ),
    ]
