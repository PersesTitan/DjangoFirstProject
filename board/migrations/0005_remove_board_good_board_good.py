# Generated by Django 4.1.2 on 2022-10-11 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_remove_board_good_board_good'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='good',
        ),
        migrations.AddField(
            model_name='board',
            name='good',
            field=models.IntegerField(default=0),
        ),
    ]
