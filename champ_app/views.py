import re
import datetime
from django.contrib.auth import logout as user_logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .choices import *
from .forms import *
from .models import *
from .paypal import *
from .spreadsheet import *

def index(request):
    next_tournament = Tournament.objects.filter(date__gt=datetime.date.today()).order_by("date").first()
    return render(request,'index.html',{
        'next_tournament':next_tournament,
    })

def rules(request):
    return render(request,'rules.html',{
    })

def league_info(request):
    return render(request,'league_info.html',{
    })

def donate(request):
    return render(request,'donate.html',{
    })

def submit(request):
    if request.user.is_anonymous(): return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            game_number = request.POST['game_number']
            game_links = get_game_links(form)
            game = Game.objects.get(number=game_number)
            set_winner_loser(game,game_links)
            submit_game(game,game_links)
            return HttpResponseRedirect(reverse('submit'))
    else:
        form = SubmitForm()
    return render(request,'submit.html',{
        'form':form,
    })

def search(request,input):
    teams = Team.objects.filter(name__icontains=input)
    return render(request, 'search.html',{
        'results':teams,
    })

def logout(request):
    user_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

def tournament_payment(request,tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    return render(request,'tournament_payment.html',{
        'tournament':tournament,
    })

def tournament_signup(request,tournament_id,team_name,action):
    try:
        team = Team.objects.get(name=team_name)
        tournament = Tournament.objects.get(pk=tournament_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('tournament_page',kwargs={'tournament_id':tournament_id}))
    add_tournament(team,tournament) if action == 'add' else remove_tournament(team,tournament)

    return HttpResponseRedirect(reverse('tournament_page',kwargs={'tournament_id':tournament_id}))

def tournament_activate(request,tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    activate_tournament(tournament)
    return  HttpResponseRedirect(reverse("admin:champ_app_tournament_changelist"))

def roster_change(request):
    team_name = request.GET.get('team_name', None)
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

def get_game_links(form):
    games = {}
    for field in form.cleaned_data:
        value = form.cleaned_data[field]
        if value != '': games[field] = value
    return games

def set_winner_loser(game,game_links):
    game.winner = Team.objects.get(name=game_links['winner'])
    game.loser = Team.objects.get(name=game_links['loser'])
    game.save()

def add_tournament(team,tournament):
    enter_signup(team,tournament) # spreadsheet.py
    team.tournaments.add(tournament)
    if tournament.pay: add_payment(team,tournament)

def remove_tournament(team,tournament):
    remove_signup(team,tournament) # spreadsheet.py
    team.tournaments.remove(tournament)
    if tournament.pay: remove_payment(team,tournament)

def add_payment(team,tournament):
    p = Payment.objects.filter(team=team,tournament=tournament)
    payment = paypalrestsdk.Payment.find(p.first().ID)
    payer_id = payment['payer']['payer_info']['payer_id']
    if payment.execute({"payer_id": payer_id}):
        sale_id = payment['transactions'][0]['related_resources'][0]['sale']['id']
        p.update(sale_id=sale_id)
        p.update(paid=True)
    else:
      print(payment.error) # Error Hash

def remove_payment(team,tournament):
    p = Payment.objects.get(team=team,tournament=tournament)
    refund_payment(p) # paypal.py
    p.delete()
