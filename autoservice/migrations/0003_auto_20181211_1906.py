# Generated by Django 2.1.4 on 2018-12-11 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0002_auto_20181206_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Модель')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Марка')),
            ],
            options={
                'verbose_name': 'Марка автомобиля',
                'verbose_name_plural': 'Марки автомобилей',
            },
        ),
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Тип автомобиля',
                'verbose_name_plural': 'Типы автомобилей',
            },
        ),
        migrations.AlterField(
            model_name='worktype',
            name='norm_hour',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Нормо-час'),
        ),
        migrations.AddField(
            model_name='car',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservice.CarBrand'),
        ),
        migrations.AddField(
            model_name='car',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.CarType'),
        ),
        migrations.AddField(
            model_name='worktype',
            name='car_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.CarType'),
        ),
    ]
