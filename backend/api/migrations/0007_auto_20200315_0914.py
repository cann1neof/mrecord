# Generated by Django 3.0.3 on 2020-03-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_mkb_parser'),
    ]

    operations = [
        migrations.CreateModel(
            name='MKB_DB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(max_length=4)),
                ('name', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='MKB_Parser',
        ),
    ]
