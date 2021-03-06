# Generated by Django 3.0.5 on 2020-05-15 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('specification', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.TextField()),
                ('address', models.TextField()),
                ('delivery_type', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.IntegerField()),
                ('specification', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('name', models.TextField()),
                ('distributor', models.TextField()),
                ('info', models.TextField()),
                ('price', models.IntegerField()),
                ('selector', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Order'),
        ),
    ]
