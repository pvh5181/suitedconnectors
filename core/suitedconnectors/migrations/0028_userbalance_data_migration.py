# Generated by Django 2.0.8 on 2018-09-29 00:43
from django.db import migrations

from banker.utils import balance


def create_user_balance(apps, schema_editor):
    """Method to create UserBalance for existing users"""
    User = apps.get_model('suitedconnectors', 'User')
    UserBalance = apps.get_model('suitedconnectors', 'UserBalance')
    for user in User.objects.all().only('id'):
        UserBalance.objects.get_or_create(user=user, balance=balance(user))


class Migration(migrations.Migration):

    dependencies = [
        ('suitedconnectors', '0027_userbalance'),
    ]

    operations = [
        migrations.RunPython(create_user_balance)
    ]
