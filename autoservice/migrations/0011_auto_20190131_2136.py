# Generated by Django 2.1.4 on 2019-01-31 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0010_auto_20190113_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worktype',
            options={'verbose_name': 'Вид работы по автомобилям', 'verbose_name_plural': 'Виды работ по автомобилям'},
        ),
    ]
