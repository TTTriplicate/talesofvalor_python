# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-31 01:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('characters', '0002_auto_20170530_2045'),
        ('events', '0002_auto_20170530_2045'),
        ('players', '0001_initial'),
        ('skills', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BetweenGameSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('question', djangocms_text_ckeditor.fields.HTMLField()),
                ('answer', djangocms_text_ckeditor.fields.HTMLField(blank=True)),
                ('submit_date', models.DateTimeField(auto_now=True, verbose_name='submitted')),
                ('answer_date', models.DateTimeField(editable=False, verbose_name='answered')),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='players.Player')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.Character')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skills.Skill')),
            ],
        ),
    ]
