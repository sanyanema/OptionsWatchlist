# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # Table List File 
    path('ui-tables.html/<slug:ticker>', views.tables, name='ui-tables.html'),

    # Maps (Price Chart) File 
    path('ui-maps.html/<slug:ticker>', views.maps, name='ui-maps.html'),

    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
]
