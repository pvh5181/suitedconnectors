# Generated by Django 2.0.8 on 2018-12-27 22:00

from django.db import migrations
from django.db.models import Q

from poker.constants import (
    CASH_GAME_BBS, N_BB_TO_NEXT_LEVEL,
    TOURNEY_BUYIN_AMTS, TOURNEY_BUYIN_TIMES
)


def user_earned_chips(apps, user_id) -> float:
    User = apps.get_model('suitedconnectors', 'User')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    user_type = ContentType.objects.get_for_model(User)
    user_transfers = Q(source_id=user_id) & Q(dest_type=user_type)\
        | Q(source_type=user_type) & Q(dest_id=user_id)

    BalanceTransfer = apps.get_model('banker', 'BalanceTransfer')
    transfers = BalanceTransfer.objects.filter(
        Q(source_id=user_id) | Q(dest_id=user_id),
    ).exclude(
        user_transfers
    ).order_by('timestamp')

    total = 0
    for transfer in transfers:
        if transfer.dest_id == user_id:
            total += transfer.amt
        else:
            total -= transfer.amt
        if total < 0:
            total = 0

    return total


def calculated_levels(apps, user_id, userstats):
    earned_chips = user_earned_chips(apps, user_id)
    cash_lvl = earned_chips / N_BB_TO_NEXT_LEVEL
    tourney_lvl = earned_chips / TOURNEY_BUYIN_TIMES

    return {
        'cashtables_level': max(
            (lvl for lvl in CASH_GAME_BBS if lvl < cash_lvl),
            default=CASH_GAME_BBS[0]
        ),
        'tournaments_level': max(
            (lvl for lvl in TOURNEY_BUYIN_AMTS if lvl < tourney_lvl),
            default=TOURNEY_BUYIN_AMTS[0]
        ),
    }


def create_user_levels(apps, schema_editor):
    """Method to create user levels for existing users"""
    User = apps.get_model('suitedconnectors', 'User')
    UserStats = apps.get_model('suitedconnectors', 'UserStats')

    for user in User.objects.all().only('id'):
        if not user.is_robot:
            userstats, _ = UserStats.objects.get_or_create(user=user)

            calc_levels = calculated_levels(apps, user.id, userstats).items()
            for lvl_type, lvl_amt in calc_levels:
                setattr(userstats, lvl_type, lvl_amt)

            userstats.save()


class Migration(migrations.Migration):

    dependencies = [
        ('suitedconnectors', '0035_auto_20181226_0244'),
    ]

    operations = [
        migrations.RunPython(create_user_levels)
    ]
