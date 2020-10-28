from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("v1", views.v1, name="v1"),
    path('', views.home, name="home"),
	path('help', views.help, name = 'help'),
	path('about_us', views.about_us, name = 'about_us'),
	path('contact', views.contact, name = 'contact'),
	path('visualization', views.visualization, name = 'visualization'),
	path('view', views.view, name="index"),
	path("<int:id>", views.index, name="index"),
]