# Generated by Django 3.0.4 on 2020-04-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20200401_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='code',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
