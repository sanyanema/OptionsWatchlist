from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(response):
    return render(response, "main/index.html", {'name' : "John Smith"})
    
def v1(response):
    return HttpResponse("<h1>v1</h1>")

def home(request):
	return render(request, 'main/home.html', {'name' : "John Smith", 'stock' : "Apple"})

def help(request):
	return render(request, 'main/help.html', {'name' : "John Smith"})

def about_us(request):
	return render(request, 'main/about_us.html', {'name' : "John Smith"})

def contact(request):
	return render(request, 'main/contact.html', {'name' : "John Smith"})

def visualization(request):
	return render(request, 'main/visualization.html', {'stock' : "Apple"})
    
    
