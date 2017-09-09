from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import *

class Stats(models.Model):
    points = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0
    )
    wins = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0
    )
    losses = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0
    )
    ties = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0
    )

class Team(models.Model):
    # eligible = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    captain = models.CharField(max_length=30)
    player1 = models.CharField(
        max_length=30,
        blank=True,null=True
    )
    player2 = models.CharField(
        max_length=30,
        blank=True,null=True
    )
    player3 = models.CharField(
        max_length=30,
        blank=True,null=True
    )
    player4 = models.CharField(
        max_length=30,
        blank=True,null=True
    )
    stats = models.OneToOneField(Stats)
    server = models.IntegerField(
        choices=SERVER_CHOICES,
        verbose_name='Server',
    )
    logo = models.ImageField(
        'logo',
        max_length=100,
        upload_to='photos',
        blank=True
    )

    class Meta:
        db_table = 'rosters'
    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(verbose_name='Email',max_length=255)
    team = models.OneToOneField(
        Team,
        on_delete=models.SET_NULL,
        blank=True,null=True
    )

    def __str__(self):
        return self.email
