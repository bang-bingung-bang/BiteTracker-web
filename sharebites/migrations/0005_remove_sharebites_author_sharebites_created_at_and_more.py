# Generated by Django 5.1.2 on 2024-10-24 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import now


class Migration(migrations.Migration):

    dependencies = [
        ('sharebites', '0004_remove_comment_date_commented_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharebites',
            name='author',
        ),
        migrations.AddField(
            model_name='sharebites',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sharebites',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
