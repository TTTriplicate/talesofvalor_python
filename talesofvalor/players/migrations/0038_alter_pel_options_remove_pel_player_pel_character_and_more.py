# Generated by Django 4.2.10 on 2024-03-23 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0026_alter_character_created_by_and_more'),
        ('players', '0037_alter_registration_registration_request'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pel',
            options={'ordering': ('-event',)},
        ),
        migrations.RemoveField(
            model_name='pel',
            name='player',
        ),
        migrations.AddField(
            model_name='pel',
            name='character',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='characters.character'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pel',
            name='devout',
            field=models.TextField(blank=True, default='', verbose_name='If you are Devout or Supplicant to a faith, please tell us \n        how you practiced and demonstrated your beliefs.'),
        ),
        migrations.AlterField(
            model_name='pel',
            name='learned',
            field=models.TextField(blank=True, default='', verbose_name='Did your character learn new skills or spells during game?  \n        If so, list them here.'),
        ),
        migrations.AlterField(
            model_name='pel',
            name='new_rule_dislikes',
            field=models.TextField(blank=True, default='', verbose_name="Is there anything you didn't care for about the new rules and\n        systems and what do you think would improve it?"),
        ),
        migrations.AlterField(
            model_name='pel',
            name='new_rule_likes',
            field=models.TextField(blank=True, default='', verbose_name="Is there anything you really liked about the new rules and\n        systems we've implemented?"),
        ),
        migrations.AlterField(
            model_name='pel',
            name='plans',
            field=models.TextField(blank=True, default='', verbose_name="What are you character's current interests and plans? What do\n        you think you'll be working on moving forward?"),
        ),
    ]