# Generated by Django 4.0.5 on 2022-07-11 08:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market', '0004_alter_country_iso_alpha_2_alter_country_iso_alpha_3'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название счета')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_price', models.DecimalField(decimal_places=6, max_digits=16, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='app.account', verbose_name='Счет')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='market.asset', verbose_name='Актив')),
            ],
            options={
                'verbose_name': 'Позиция',
                'verbose_name_plural': 'Позиции',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('commission', models.DecimalField(decimal_places=6, default=0, max_digits=12, verbose_name='Комиссия')),
                ('type_operation', models.CharField(choices=[('Купить', 'BUY'), ('Продать', 'SELL'), ('Пополнить', 'INPUT'), ('Вывести', 'OUTPUT'), ('Дивиденд', 'DIVIDEND'), ('Купон', 'COUPON')], max_length=63, verbose_name='Тип операции')),
                ('date', models.DateTimeField(default=datetime.datetime.today, verbose_name='Дата операции')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='app.account', verbose_name='Счет')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='market.asset', verbose_name='Актив')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.currency', verbose_name='Валюта операции')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
            },
        ),
        migrations.CreateModel(
            name='AccountHistoricalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата состояния')),
                ('total_invested', models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Всего инвестировано')),
                ('turnover', models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Оборот средств')),
                ('total_amount', models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Общая стоимость')),
                ('total_profit', models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Общая')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='app.account')),
            ],
            options={
                'verbose_name': 'Состояние',
                'verbose_name_plural': 'Состояния',
            },
        ),
    ]
