# Generated by Django 3.0.4 on 2020-04-12 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_permissiontoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeysToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=256)),
                ('public_key', models.CharField(max_length=442)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(blank=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
        ),
        migrations.DeleteModel(
            name='PermissionToken',
        ),
    ]