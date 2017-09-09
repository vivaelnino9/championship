from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from champ_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^team/(?P<team_name>[\w|\W]+)/$',views.team, name='team'),
]
