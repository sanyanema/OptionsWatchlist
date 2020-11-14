from django.shortcuts import render, redirect
from django.http import HttpResponse

def table(response):
	return render(request, 'templates/ui-tables.html', {name: 'Testing'})