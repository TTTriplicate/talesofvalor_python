# Generated by Django 3.2.17 on 2023-12-14 18:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0037_alter_registration_registration_request'),
        ('betweengameabilities', '0002_alter_betweengameability_ability'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='betweengameability',
            options={'verbose_name': 'Between Game Ability', 'verbose_name_plural': 'Between Game Abilities'},
        ),
        migrations.RemoveField(
            model_name='betweengameability',
            name='submit_date',
        ),
        migrations.AddField(
            model_name='betweengameability',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='submitted'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='betweengameability',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='betweengameabilities_betweengameability_author', to='players.player'),
        ),
        migrations.AddField(
            model_name='betweengameability',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last updated'),
        ),
        migrations.AddField(
            model_name='betweengameability',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='betweengameabilities_betweengameability_updater', to='players.player'),
        ),
    ]
