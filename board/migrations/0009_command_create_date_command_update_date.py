# Generated by Django 4.1.2 on 2022-10-11 05:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_command_alter_board_command'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='command',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
