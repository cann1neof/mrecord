# Generated by Django 3.0.5 on 2020-05-18 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20200517_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=32, unique=True),
        ),
    ]
