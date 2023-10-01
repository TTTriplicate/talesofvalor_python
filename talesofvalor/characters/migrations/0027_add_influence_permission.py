# Generated by Django 3.0.11 on 2021-09-19 22:03

from django.contrib.auth.models import Group, Permission

from django.db import migrations


def add_permission_to_group(apps, schema_editor):

    staff, created = Group.objects.get_or_create(name="Staff")
    admin, created = Group.objects.get_or_create(name="Admin")
    permissions = Permission.objects.get(codename='update_influence')
    if permissions:
        staff.permissions.add(permissions)
        admin.permissions.add(permissions)


def remove_permission_from_group(apps, schema_editor):
    staff, created = Group.objects.get_or_create(name="Staff")
    admin, created = Group.objects.get_or_create(name="Admin")
    permissions = Permission.objects.filter(codename__in=[
        'update_influence',
    ])
    if permissions.count() > 0:
        staff.permissions.remove(permissions)
        admin.permissions.remove(permissions)


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0026_alter_character_options'),
    ]

    operations = [
        migrations.RunPython(add_permission_to_group, remove_permission_from_group),
    ]


