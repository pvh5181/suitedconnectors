# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-04 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suitedconnectors', '0014_auto_20180329_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auto_rebuy_in_bbs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='four_color_deck',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='show_chat_msgs',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='show_dealer_msgs',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='show_win_msgs',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='sit_behaviour',
            field=models.CharField(choices=[('nothing', 'NOTHING'), ('auto_next_hand', 'AUTO NEXT HAND'), ('auto_bb', 'AUTO BB')], default='nothing', max_length=20),
        ),
    ]
