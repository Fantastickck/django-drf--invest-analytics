# Generated by Django 4.0.5 on 2022-07-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_currencycourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='type_currency',
            field=models.CharField(choices=[('Валюта', 'CURRENCY'), ('Криптовалюта', 'CRYPTOCURRENCY')], default=0, max_length=20, verbose_name='Тип валюты'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currencycourse',
            name='value',
            field=models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Курс'),
        ),
    ]
