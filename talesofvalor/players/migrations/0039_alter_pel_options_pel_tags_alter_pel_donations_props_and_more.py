# Generated by Django 4.2.16 on 2024-10-05 01:04

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('players', '0038_alter_pel_options_remove_pel_player_pel_character_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pel',
            options={'ordering': ('-event', '-created')},
        ),
        migrations.AddField(
            model_name='pel',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='pel',
            name='donations_props',
            field=models.TextField(blank=True, default='', verbose_name='Donations (Props/funds/or other materials.'),
        ),
        migrations.AlterField(
            model_name='pel',
            name='donations_time',
            field=models.TextField(blank=True, default='', verbose_name='Donations (Time spent doing set up / breakdown.'),
        ),
    ]
