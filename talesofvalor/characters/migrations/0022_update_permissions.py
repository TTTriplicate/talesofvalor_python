# Generated by Django 3.2.17 on 2023-07-02 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0021_remove_character_skills'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='character',
            options={'permissions': (('reset_points', 'Can reset points'), )},
        ),
    ]