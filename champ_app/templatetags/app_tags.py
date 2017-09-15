from django import template

from champ_app.models import *

register = template.Library()

@register.simple_tag(name='get_players')
# get players from team
def get_players(team,include_fields):
    return team.get_players(include_fields)

@register.simple_tag(name='field_needed')
# get field needed if team has less than 5 players
def field_needed(team):
    model_fields = ['captain','player1','player2','player3','player4']
    team_fields = team.get_players(True).keys()
    for field in model_fields:
        if field not in team_fields: return field
    return ''
