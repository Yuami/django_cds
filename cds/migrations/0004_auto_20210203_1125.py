# Generated by Django 3.1.6 on 2021-02-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cds', '0003_auto_20210203_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
    ]
