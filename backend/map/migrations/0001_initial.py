# Generated by Django 3.0.5 on 2020-05-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48)),
                ('additional', models.TextField()),
                ('coords', models.CharField(max_length=48)),
            ],
        ),
    ]
