# Generated by Django 4.0.5 on 2022-07-08 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('abbreviation', models.CharField(max_length=10, verbose_name='Аббревиатура')),
                ('symbol', models.CharField(max_length=10, verbose_name='Символ')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Биржа')),
            ],
            options={
                'verbose_name': 'Биржа',
                'verbose_name_plural': 'Биржи',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Сектор',
                'verbose_name_plural': 'Секторы',
            },
        ),
        migrations.CreateModel(
            name='TypeAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип актива',
                'verbose_name_plural': 'Типы активов',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('ticker', models.CharField(max_length=10, verbose_name='Тикер')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.country', verbose_name='Страна')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.currency', verbose_name='Валюта')),
                ('market', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.market', verbose_name='Биржа')),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.sector', verbose_name='Сектор')),
                ('type_asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.typeasset', verbose_name='Тип актива')),
            ],
            options={
                'verbose_name': 'Актив',
                'verbose_name_plural': 'Активы',
            },
        ),
    ]