import re

from django.contrib.auth import logout as user_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .choices import *
from .forms import *
from .models import *

def index(request):
    return render(request,'index.html',{
    })

def logout(request):
    user_logout(request)
    return HttpResponseRedirect('/')

def tournaments(request):
    return render(request,'tournaments.html',{
    })

def team(request,team_name):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = make_team(form,request)
            return HttpResponseRedirect('/team/'+team.name)
    else:
        form = TeamForm()
    return render(request,'team_page.html',{
        'form':form,
    })

####### HELPER FUNCTIONS #######

def make_team(form,request):
    team = form.save(commit=False)
    team.stats = Stats.objects.create()
    team.save()
    User.objects.filter(email=request.user.email).update(team=team)
    return team
