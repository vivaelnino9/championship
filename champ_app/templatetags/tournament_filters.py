from django import template

from champ_app.models import *

register = template.Library()

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

@register.filter(name='can_signup')
# check if user can sign up for tournament
def can_signup(user,tournament):
    if user.is_anonymous() or user.team is None: return False
    return user.team not in tournament.team_set.all()
