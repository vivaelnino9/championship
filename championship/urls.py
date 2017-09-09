from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('champ_app.urls')),
    url('', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
]
