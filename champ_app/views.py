import json
import requests
from requests.auth import HTTPBasicAuth

from django.shortcuts import render

def index(request):
    # title = '''{
    #     "title":"TagPro Championship Series"
    # }'''
    # tour_data = json.loads(title)
    # tournament = requests.put('https://bracketcloud.com/api/1.0/tournaments/103815?api_key=735b93738ff58c279fb465be2404dcc10dc6db8d',json=tour_data)
    return render(request,'index.html',{
        # 'tournament':tournament.text,
    })

def registration(request):
    return render(request,'registration.html')
