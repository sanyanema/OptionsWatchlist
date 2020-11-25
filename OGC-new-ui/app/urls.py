# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # General Table List File
    path('ui-tables.html/', views.pages, name='ui-tables.html'),

    # Table List File for a specific ticker
    path('ui-tables.html/<slug:ticker>', views.tables, name='ui-tables.html'),

    # General Table List File
    path('ui-maps.html/', views.pages, name='ui-maps.html'),

    # Maps (Price Chart) File 
    path('ui-maps.html/<slug:ticker>', views.maps, name='ui-maps.html'),

    # Get the Greeks for a Contract
    path('contract/<slug:contract>', views.contract, name='contract.html'),

    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
]
