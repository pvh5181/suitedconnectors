# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-14 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suitedconnectors', '0016_user_show_spectator_msgs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='played_first_tournament',
            field=models.BooleanField(default=False),
        ),
    ]
