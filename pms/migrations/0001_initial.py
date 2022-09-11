# Generated by Django 3.2.15 on 2022-09-11 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField(default=datetime.date.today)),
                ('stock', models.IntegerField(default=1)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]