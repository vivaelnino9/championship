import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import *

class Tournament(models.Model):
    name = models.CharField(verbose_name="Name",max_length=50)
    abv = models.CharField(verbose_name="Abbreviation",max_length=10)
    full = models.CharField(verbose_name="Full Name",max_length=50)
    pay = models.BooleanField(verbose_name="Pay",default=False)
    cost = models.CharField(
        verbose_name="Cost",
        max_length=10,
        blank=True,null=True)
    server = models.IntegerField(
        verbose_name="Server",
        choices=SERVER_CHOICES,
    )
    date = models.DateField(default=datetime.date.today)
    logo = models.ImageField(
        'logo',
        max_length=100,
        upload_to='photos',
        blank=True
    )
    Qualified = models.ManyToManyField(
        "champ_app.Team",
        verbose_name="Qualified Teams",
        blank=True
    )

    class Meta:
        db_table = "tournaments"
    def __str__(self):
        return self.name

class Payment(models.Model):
    team = models.ForeignKey(
        "champ_app.Team",
        verbose_name='Team',
        related_name='team_payment',
        null=True,
        on_delete=models.CASCADE
    )
    ID = models.CharField(verbose_name="ID",max_length=50)
    sale_id = models.CharField(
        verbose_name="Sale ID",
        max_length=50,
        blank=True,null=True
    )
    amount = models.CharField(
        verbose_name="Amount",
        max_length=50,
        blank=True,null=True
    )
    paid = models.BooleanField(verbose_name="Paid",default=False)
    approval_url = models.CharField(verbose_name="Approval Url",max_length=200)
    tournament = models.ForeignKey(
        Tournament,
        verbose_name='Tournament',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.ID

class Team(models.Model):
    name = models.CharField(verbose_name="Name",max_length=50)
    captain = models.CharField(verbose_name="Captain",max_length=30)
    player1 = models.CharField(
        verbose_name="Player 1",
        max_length=30,
        blank=True,null=True
    )
    player2 = models.CharField(
        verbose_name="Player 2",
        max_length=30,
        blank=True,null=True
    )
    player3 = models.CharField(
        verbose_name="Player 3",
        max_length=30,
        blank=True,null=True
    )
    player4 = models.CharField(
        verbose_name="Player 4",
        max_length=30,
        blank=True,null=True
    )
    server = models.IntegerField(
        verbose_name="Server",
        choices=SERVER_CHOICES,
    )
    logo = models.ImageField(
        verbose_name="Logo",
        max_length=100,
        upload_to='photos',
        blank=True
    )
    tournaments = models.ManyToManyField(
        Tournament,
        verbose_name="Tournaments",
        blank=True
    )

    class Meta:
        db_table = "rosters"
    def __str__(self):
        return self.name

    def get_players(self,include_fields):
        # get players on team, specify wether returned result needs to be in a
        # dict or list depending on the need for field names
        team_fields = Team.objects.filter(name=self.name).values()
        avoid = ['id','name','stats_id','server','logo']
        players_dict = {}
        players_list = []
        for fields in team_fields:
            for field,value in fields.items():
                if value and field not in avoid:
                    players_dict[field] = value if include_fields else players_list.append(value)
        if include_fields: return players_dict
        else: return players_list

    def get_payment(self,tournament):
        return Payment.objects.filter(team=self,tournament=tournament)

class User(AbstractUser):
    email = models.EmailField(verbose_name="Email",max_length=255)
    team = models.OneToOneField(
        Team,
        verbose_name="Team",
        on_delete=models.SET_NULL,
        blank=True,null=True
    )

    def __str__(self):
        return self.email
