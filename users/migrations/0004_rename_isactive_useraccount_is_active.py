# Generated by Django 5.1.6 on 2025-04-18 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_is_active_useraccount_isactive_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='isActive',
            new_name='is_active',
        ),
    ]
