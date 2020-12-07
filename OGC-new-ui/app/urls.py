from django.urls import path, re_path
from app import views

urlpatterns = [
    # Table List File for a specific ticker
    path('options/<slug:ticker>', views.options, name='options_stock.html'),

    # Maps (Price Chart) File 
    path('stock_info/<slug:ticker>', views.stock, name='stock.html'),

    # Get the Greeks for a Contract
    path('contract/<slug:contract>', views.contract, name='contract.html'),

    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
]
