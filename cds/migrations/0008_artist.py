# Generated by Django 3.1.6 on 2021-02-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cds', '0007_auto_20210204_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('death_date', models.DateField(blank=True, null=True)),
                ('bands', models.ManyToManyField(to='cds.Band')),
            ],
        ),
    ]
