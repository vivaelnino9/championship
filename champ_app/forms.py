import collections

from django import forms
from django.utils.translation import gettext as _
from .models import *
from .choices import *
from .spreadsheet import *

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

        if Team.objects.filter(name=cleaned_data.get('name')).exists():
            msg = 'That team name is already being used by another team!'
            self.add_error('name', msg)

        players = {
            'captain':cleaned_data.get('captain'),
            'player1':cleaned_data.get('player1'),
            'player2':cleaned_data.get('player2'),
            'player3':cleaned_data.get('player3'),
            'player4':cleaned_data.get('player4')
        }
        self.check_players(players)

        return cleaned_data

    def check_players(self,players):
        existing_players = self.get_existing_players()
        for field,player in players.items():
            msg = player + ' is not available! Player might be on another team or already listed'
            self.add_error(field, msg) if player in existing_players else existing_players.append(player)

    def get_existing_players(self):
        existing_players = []
        for team in Team.objects.all():
            for player in team.get_players(False):
                existing_players.append(player)
        return existing_players

class SubmitForm(forms.Form):
    g1h1 = forms.CharField(
        max_length=50,
        label="G1H1",
    )
    g1h1time = forms.CharField(
        max_length=50,
        label="G1H1[Time]",
        required=False
    )
    g1h2 = forms.CharField(
        max_length=50,
        label="G1H2",
    )
    g1h2time = forms.CharField(
        max_length=50,
        label="G1H2[Time]",
        required=False
    )
    g1ot1 = forms.CharField(
        max_length=50,
        label="G1OT1",
        required=False
    )
    g1ot2 = forms.CharField(
        max_length=50,
        label="G1OT2",
        required=False
    )
    g2h1 = forms.CharField(
        max_length=50,
        label="G2H1",
    )
    g2h1time = forms.CharField(
        max_length=50,
        label="G2H1[Time]",
        required=False
    )
    g2h2 = forms.CharField(
        max_length=50,
        label="G2H2",
    )
    g2h2time = forms.CharField(
        max_length=50,
        label="G2H2[Time]",
        required=False
    )
    g2ot1 = forms.CharField(
        max_length=50,
        label="G2OT1",
        required=False
    )
    g2ot2 = forms.CharField(
        max_length=50,
        label="G2OT2",
        required=False
    )
    winner = forms.CharField(
        max_length=50,
        label="Winner",
    )
    loser = forms.CharField(
        max_length=50,
        label="Loser",
    )
