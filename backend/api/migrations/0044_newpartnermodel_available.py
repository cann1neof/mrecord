# Generated by Django 3.0.5 on 2020-05-17 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20200517_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='newpartnermodel',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
