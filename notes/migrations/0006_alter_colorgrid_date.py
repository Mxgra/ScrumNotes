# Generated by Django 4.1.7 on 2023-03-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_colorgrid_day_has_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colorgrid',
            name='date',
            field=models.DateField(unique=True, verbose_name='date'),
        ),
    ]