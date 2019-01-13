# Generated by Django 2.1.4 on 2019-01-10 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0003_auto_20181211_1906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AddField(
            model_name='work',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='autoservice.Car', verbose_name='Автомобиль'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservice.CarBrand', verbose_name='Марка'),
        ),
        migrations.AlterField(
            model_name='car',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.CarType', verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.Position', verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservice.Employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='work',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservice.Client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='work',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservice.Employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='work',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservice.WorkType', verbose_name='Вид работы'),
        ),
        migrations.AlterField(
            model_name='worktype',
            name='car_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.CarType', verbose_name='Тип автомобиля'),
        ),
    ]