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
        'tournament':tournament
    })

def tournament_signup(request):
    team_name = request.GET.get('team_name', None)
    tournament = request.GET.get('tournament', None)
    enter_signup(team_name,tournament) # spreadsheet.py
    data = {'team_name':team_name,'tournament':tournament }
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
            return HttpResponseRedirect('/team/'+team.name)
    else:
        form = TeamForm()
    return render(request,'team_page.html',{
        'team':team,
        'form':form,
    })

####### HELPER FUNCTIONS #######
