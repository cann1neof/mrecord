# Generated by Django 3.0.5 on 2020-04-28 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20200426_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
