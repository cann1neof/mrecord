# Generated by Django 3.0.4 on 2020-04-19 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hospital',
        ),
    ]
