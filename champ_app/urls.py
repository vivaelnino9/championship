from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from champ_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^rules/$', views.rules, name='rules'),
    url(r'^league_info/$', views.league_info, name='league_info'),
    url(r'^team/(?P<team_name>[\w|\W]+)/$',views.team, name='team'),
    url(r'^tournaments/$',views.tournaments, name='tournaments'),
    url(r'^tournaments/(?P<tournament_id>[\w|\W]+)/$',views.tournament_page, name='tournament_page'),
    url(r'^tournament_payment/(?P<tournament_id>[\w|\W]+)/$',views.tournament_payment, name='tournament_payment'),
    url(r'^tournament_signup/(?P<tournament_id>[\w|\W]+)/(?P<team_name>[\w|\W]+)/(?P<action>[\w|\W]+)/$', views.tournament_signup, name='tournament_signup'),
    url(r'^roster_change/$', views.roster_change, name='roster_change'),
]
