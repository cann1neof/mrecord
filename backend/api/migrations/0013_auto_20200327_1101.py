# Generated by Django 3.0.4 on 2020-03-27 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_unregistered_record'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unregistered_record',
            old_name='auth_code',
            new_name='code',
        ),
    ]
