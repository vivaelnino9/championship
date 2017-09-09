from django import forms
from django.contrib import admin

from .models import *

class UserAdminForm(forms.ModelForm):
    model = User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','last_name')
    search_fields = ['email',]
    list_filter = []
    list_per_page = 20
    form = UserAdminForm

admin.site.register(User,UserAdmin)

class TeamAdminForm(forms.ModelForm):
    model = Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','server')
    search_fields = ['name','captain','player1','player2','player3','player4','player5']
    list_filter = ['server']
    list_per_page = 20
    form = TeamAdminForm

admin.site.register(Team,TeamAdmin)
