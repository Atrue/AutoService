# Generated by Django 2.1.4 on 2019-01-13 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0008_auto_20190113_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservice.CarGeneration', verbose_name='Автомобиль'),
        ),
    ]
