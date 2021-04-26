from django.urls import path
from django.conf.urls import url

from . import views

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^movie/input/$',views.movieInput),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]