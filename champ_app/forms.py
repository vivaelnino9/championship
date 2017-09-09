from django import forms

from .models import *
from .choices import *

class TeamForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    captain = forms.CharField(max_length=30)
    player1 = forms.CharField(max_length=30)
    player2 = forms.CharField(max_length=30)
    player3 = forms.CharField(max_length=30)
    player4 = forms.CharField(max_length=30,required=False)
    server = forms.ChoiceField(choices=SERVER_CHOICES)
    class Meta:
        model = Team
        fields = ('name','captain','player1','player2','player3','player4','server')

    def clean(self):
        cleaned_data = super(TeamForm, self).clean()
        name = cleaned_data.get('name')
        captain = cleaned_data.get('captain')
        player1 = cleaned_data.get('player1')
        player2 = cleaned_data.get('player2')
        player3 = cleaned_data.get('player3')
        player4 = cleaned_data.get('player4')
        server = cleaned_data.get('server')

        if Team.objects.filter(name=name).exists():
            msg = 'That team name is already being used by another team!'
            self.add_error('name', msg)

        players = {
            'captain':captain,'player1':player1,'player2':player2,
            'player3':player3,'player4':player4
        }

        for field,player in players.items():
            if player in self.get_existing_players():
                msg = player+ ' is already on another team!'
                self.add_error(field, msg)
        return cleaned_data

    def get_existing_players(self):
        team_fields = Team.objects.all().values()
        avoid = ['id','name','stats_id','server','logo']
        existing_players = []
        for fields in team_fields:
            for field,value in fields.items():
                if value and field not in avoid:
                    existing_players.append(value)
        return existing_players
