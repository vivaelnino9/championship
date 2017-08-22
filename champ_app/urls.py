from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from champ_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
