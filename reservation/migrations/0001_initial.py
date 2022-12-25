# Generated by Django 4.1.3 on 2022-11-22 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField()),
                ('places', models.IntegerField()),
                ('form', models.BooleanField()),
                ('coordinates', models.CharField(max_length=7)),
                ('size', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('data', models.DateField()),
                ('table_number', models.ManyToManyField(to='reservation.tables')),
            ],
        ),
    ]