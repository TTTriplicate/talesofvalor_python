# Generated by Django 3.2.17 on 2023-10-24 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0012_alter_skill_options'),
        ('characters', '0024_alter_character_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='skills',
            field=models.ManyToManyField(through='characters.CharacterSkills', to='skills.HeaderSkill'),
        ),
    ]