# Generated by Django 3.2.11 on 2022-04-13 03:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='last_bump',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]