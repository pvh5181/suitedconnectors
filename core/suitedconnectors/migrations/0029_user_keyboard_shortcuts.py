# Generated by Django 2.0.8 on 2018-10-10 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suitedconnectors', '0028_userbalance_data_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='keyboard_shortcuts',
            field=models.BooleanField(default=True),
        ),
    ]
