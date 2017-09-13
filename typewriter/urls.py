# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import index, parse

app_name="typewriter"

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^parse$', parse, name='parse'),
]
