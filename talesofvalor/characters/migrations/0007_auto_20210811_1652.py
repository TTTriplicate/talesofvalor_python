# Generated by Django 3.0.11 on 2021-08-11 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0006_auto_20190915_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='cp_available',
            field=models.PositiveIntegerField(default=20),
        ),
    ]