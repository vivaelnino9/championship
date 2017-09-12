from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from champ_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^team/(?P<team_name>[\w|\W]+)/$',views.team, name='team'),
    url(r'^tournaments/$',views.tournaments, name='tournaments'),
    url(r'^tournaments/(?P<tournament_id>[\w|\W]+)/$',views.tournament_page, name='tournament_page'),
    url(r'^tournament_signup/$', views.tournament_signup, name='tournament_signup'),
]
