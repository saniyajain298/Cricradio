# Generated by Django 5.1.3 on 2024-11-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_alter_series_tp_alter_series_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='status',
            field=models.CharField(max_length=100),
        ),
    ]