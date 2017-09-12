from django import template
from django.core.exceptions import ObjectDoesNotExist

from champ_app.models import *

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
