# Generated by Django 4.2.10 on 2024-03-20 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('comments', '0004_merge_20240312_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'characters'), ('model', 'Character')), models.Q(('app_label', 'events'), ('model', 'Event')), models.Q(('app_label', 'attendance'), ('model', 'Attendance')), models.Q(('app_label', 'betweengameabilities'), ('model', 'betweengameability')), models.Q(('app_label', 'origins'), ('model', 'Origin')), models.Q(('app_label', 'players'), ('model', 'Pel')), models.Q(('app_label', 'players'), ('model', 'Player')), models.Q(('app_label', 'skills'), ('model', 'Header')), models.Q(('app_label', 'skills'), ('model', 'Skill')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]