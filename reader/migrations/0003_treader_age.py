# Generated by Django 3.1.4 on 2020-12-31 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_reader_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='treader',
            name='age',
            field=models.IntegerField(default=12),
        ),
    ]