# Generated by Django 3.0.11 on 2021-07-19 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0016_auto_20210717_2323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pel',
            old_name='best_moments',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='pel',
            old_name='dislikes',
            new_name='favorites',
        ),
        migrations.RenameField(
            model_name='pel',
            old_name='likes',
            new_name='suggestions',
        ),
        migrations.RemoveField(
            model_name='pel',
            name='worst_moments',
        ),
    ]
