# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import index, parse, frame

app_name="typewriter"

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^parse$', parse, name='parse'),
    url(r'^frame$', frame, name='frame'),
    #url(r'^upload/$', UploadView.as_view(), name='upload'),
    #url(r'^delete/(?P<uid>[0-9a-fA-F]+)$', delete, name='delete'),
]
