from django import template
from django.core.exceptions import ObjectDoesNotExist

from champ_app.models import *
from champ_app.spreadsheet import *

register = template.Library()

# Team Page

@register.filter(name='has_no_team')
# check if user has a registered team
def has_no_team(user,team):
    if user.is_anonymous(): return False
    return user.team is None and team is None

@register.filter(name='can_edit')
# check if user can edit team page
def can_edit(user,team):
    if user.is_anonymous(): return False
    return user.team == team and user.team.tournaments.count() == 0

# Roster Table

@register.filter(name='can_add_player')
# check if team can add a player
def can_add_player(team):
    players = team.get_players(True)
    fields =['captain','player1','player2','player3','player4']
    for field in fields:
        if field not in players.keys():
            return True
    return False

@register.filter(name='required')
# check field is required
def required(field):
    if field.name != 'player4': return 'required'
    else: return ''
