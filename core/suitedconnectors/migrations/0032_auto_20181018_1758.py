# Generated by Django 2.0.8 on 2018-10-18 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suitedconnectors', '0031_userstats_data_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='keyboard_shortcuts',
            field=models.BooleanField(default=False),
        ),
    ]
