# Generated by Django 4.0.5 on 2022-07-08 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='iso_alpha2',
            field=models.CharField(max_length=2, null=True, verbose_name='ISO Alpha-2'),
        ),
        migrations.AddField(
            model_name='country',
            name='iso_alpha3',
            field=models.CharField(max_length=3, null=True, verbose_name='ISO Alpha-3'),
        ),
        migrations.AddField(
            model_name='country',
            name='iso_number',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='ISO число'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.country', verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='market',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.market', verbose_name='Биржа'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.sector', verbose_name='Сектор'),
        ),
    ]
