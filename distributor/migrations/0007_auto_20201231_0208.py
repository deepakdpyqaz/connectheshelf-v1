# Generated by Django 3.1.4 on 2020-12-31 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0006_auto_20201230_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buybook',
            name='price',
            field=models.FloatField(default=0, null=True),
        ),
    ]