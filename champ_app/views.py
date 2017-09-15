import re

from django.contrib.auth import logout as user_logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .choices import *
from .forms import *
from .models import *
from .spreadsheet import *

def index(request):
    return render(request,'index.html',{
    })

def logout(request):
    user_logout(request)
    return HttpResponseRedirect('/')

def tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request,'tournaments.html',{
        'tournaments':tournaments
    })
def tournament_page(request,tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    return render(request,'tournament_page.html',{
        'tournament':tournament,
    })

def tournament_signup(request):
    team_name = request.GET.get('team_name', None)
    tournament_abv = request.GET.get('tournament', None)
    add = request.GET.get('add', None)
    team = Team.objects.get(name=team_name)
    tournament = Tournament.objects.get(abv=tournament_abv)
    if add == 'true':
        enter_signup(team_name,tournament_abv) # spreadsheet.py
        team.tournaments.add(tournament)
    else:
        remove_signup(team_name,tournament_abv) # spreadsheet.py
        team.tournaments.remove(tournament)
    data = {'team_name':team_name,'tournament':tournament_abv }
    return JsonResponse(data)

def roster_change(request):
    team_name = name=request.GET.get('team_name', None)
    new_players = check_for_new_players(team_name,request)
    if new_players: change_roster(team_name,new_players)
    data = {'sucess':new_players}
    return JsonResponse(data)

def team(request,team_name):
    try:
        team = Team.objects.get(name=team_name)
    except ObjectDoesNotExist:
        team = None
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            User.objects.filter(email=request.user.email).update(team=team)
            register_team(team)
            return HttpResponseRedirect('/team/'+team.name)
    else:
        form = TeamForm()
    return render(request,'team_page.html',{
        'team':team,
        'form':form,
    })

####### HELPER FUNCTIONS #######
def check_for_new_players(team_name,request):
    new_players = {}
    team = Team.objects.get(name=team_name)
    existing_players = team.get_players(True)
    for field,player in existing_players.items():
        request_player = request.GET.get(field, None)
        if request_player != player:
            new_players[field] = request_player

    new_field = request.GET.get('new_field',None)
    new_player = request.GET.get('new_player',None)
    if new_player != '' and new_player is not None:
        new_players[new_field] = new_player

    return new_players

def change_roster(team_name,new_players):
    team = Team.objects.filter(name=team_name)
    for field,player in new_players.items():
        if field == 'captain': team.update(captain=player)
        elif field == 'player1': team.update(player1=player)
        elif field == 'player2': team.update(player2=player)
        elif field == 'player3': team.update(player3=player)
        elif field == 'player4': team.update(player4=player)
        else: pass
    if new_players: edit_roster(team_name,new_players)
