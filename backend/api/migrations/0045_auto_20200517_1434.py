# Generated by Django 3.0.6 on 2020-05-17 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_newpartnermodel_available'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Unregistered_Record',
            new_name='UnregisteredRecord',
        ),
    ]