# Generated by Django 3.0.5 on 2020-05-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20200518_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keystoken',
            name='last_activity',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
