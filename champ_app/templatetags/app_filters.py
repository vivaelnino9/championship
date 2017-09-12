from django import template
from django.core.exceptions import ObjectDoesNotExist

from champ_app.models import *
from champ_app.spreadsheet import *

register = template.Library()

@register.filter(name='has_no_team')
# check if user has a registered team
def has_no_team(user,team):
    if user.is_anonymous(): return False
    return user.team is None and team is None

@register.filter(name='required')
# check field is required
def required(field):
    if field.name != 'player4': return 'required'
    else: return ''

@register.filter(name='server_city')
# return server with city
def server_city(server):
    if server == 'Radius': city = ' (Newark, NJ)'
    elif server == 'Pi': city = ' (Atlanta, GA)'
    elif server == 'Origin': city = ' (Detroit, MI)'
    elif server == 'Sphere': city = ' (Dallas, TX)'
    elif server == 'Centra': city = ' (Fremont, CA)'
    elif server == 'Orbit': city = ' (London, UK)'
    elif server == 'Chord': city = ' (Paris, FR)'
    else: city = ' (Sydney, AUS)'
    return server + city

@register.filter(name='check_signup')
# check if team is already signed up for tournament
def check_signup(team_name,tournament):
    return check_for_signup(team_name,tournament)
