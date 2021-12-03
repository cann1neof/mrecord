# Generated by Django 3.0.4 on 2020-04-24 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_migrationtoken_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='migrationtoken',
            name='parent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.User'),
            preserve_default=False,
        ),
    ]