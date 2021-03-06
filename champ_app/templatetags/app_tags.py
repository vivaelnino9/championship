from django import template
from django.core.urlresolvers import reverse

from champ_app.models import *
from champ_app.paypal import *
from champ_app.spreadsheet import *

register = template.Library()

# Home Page

@register.simple_tag(name='get_leaders')
# get stats for leaderboards
def get_leaders():
    return False
    return get_season_leaders()

# Roster Table

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

# Navigation

@register.simple_tag(name='is_on',takes_context=True)
# deteremine which nav link should be active
def is_on(context,nav_link):
    request = context['request']
    if nav_link in request.path: return 'active'

# Tournament Page

@register.simple_tag(name='signup_link',takes_context=True)
def signup_link(context,user,tournament):
    request = context['request']
    if tournament.pay:
        return request.build_absolute_uri(reverse('tournament_payment',kwargs={'tournament_id':tournament.id}))
    else:
        return request.build_absolute_uri(reverse('tournament_signup',kwargs={'tournament_id':tournament.id,'team_name':user.team.name,'action':'add'}))

@register.simple_tag(name='signup_error_fields',takes_context=True)
# get tournament signup errors based on user
def signup_error_fields(context,user,tournament):
    request = context['request']
    errors = {}
    if user.is_anonymous():
        errors['message'] = "You need to be logged in to sign up for a tournament!"
        errors['redirect_url'] = "/login/google-oauth2/?next="+request.path
        errors['button_text'] = "Sign In"
        errors['button_class'] = "sign-in"
    elif user.team is None:
        errors['message'] = "You need a registered team to sign up!"
        errors['redirect_url'] = request.build_absolute_uri(reverse('team',kwargs={'team_name': None}))
        errors['button_text'] = "Register"
        errors['button_class'] = "register"
    else:
        # Users team is signed up already
        errors['message'] = "Your team is all signed up!"
        errors['redirect_url'] = request.build_absolute_uri(reverse('tournament_signup',kwargs={'tournament_id':tournament.id,'team_name':user.team.name,'action':'remove'}))
        errors['button_text'] = "Remove"
        errors['button_class'] = "remove"
    return errors

@register.simple_tag(name='footer_message')
def footer_message(user,tournament):
    if user.is_anonymous() or user.team is None: return 'Click button to proceed'
    elif user.team.is_signed_up(tournament):
        if tournament.pay: return 'Removing sign up will refund payment in total'
        else: return 'Click to remove your sign up'
    else:
        if tournament.pay: return 'Clicking Sign up will proceed to payment page'
        else: return 'Click to sign up for tournament'
@register.simple_tag(name='paypal_payment_link',takes_context=True)
def paypal_payment_link(context,tournament):
    request = context['request']
    payment_link = get_payment_link(request,tournament)
    link = {}
    if not payment_link['error']:
        link['link'] = payment_link['link']
        link['disabled'] = ''
    else:
        link['link'] = '#'
        link['disabled'] = 'disabled'
    return link

# Submit Page
@register.simple_tag(name='get_latest_game',takes_context=True)
def get_latest_game(context):
    request = context['request']
    user = request.user
    if user.is_anonymous(): return False
    team = user.team
    tournament = team.tournaments.filter(active=True)
    if tournament.exists():
        tournament = tournament.first()
        game = check_for_game(team,tournament)
        return game
    else:
        return False
