# Generated by Django 3.0.6 on 2020-05-31 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20200519_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
