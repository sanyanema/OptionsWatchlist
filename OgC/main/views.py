from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import WatchList, Item
# Create your views here.
stock1 = "Google"
stock1b = "GOOGL"

def index(response, id):
	ls = WatchList.objects.get(id=id)

	if response.method == "POST":
		if response.POST.get("save"):
			for item in ls.item_set.all():
				if response.POST.get("c" + str(item.id))== "clicked":
					item.complete = True
				else:
					item.complete = False
				item.save()
		elif response.POST.get("newItem"):
			txt = response.POST.get("new")

			if len(txt) > 2:
				ls.item_set.create(text=txt, complete=False)
			else:
				print("invalid")
	return render(response, "main/list.html", {'ls' : "ls"})
    
def v1(response):
    return HttpResponse("<h1>v1</h1>")

def home(request):
	return render(request, 'main/home.html', {'name' : "John Smith", 'stock' : stock1})

def help(request):
	return render(request, 'main/help.html', {'name' : "John Smith"})

def about_us(request):
	return render(request, 'main/about_us.html', {'name' : "John Smith"})

def contact(request):
	return render(request, 'main/contact.html', {'name' : "John Smith"})

def visualization(request):
	return render(request, 'main/visualization.html', {'stock' : stock1, 'name' : stock1b})

def create(response):
	if response.method == "POST":
		form = CreateNewList(response.POST)

		if form.is_valid():
			n = form.cleaned_data["name"]
			w = WatchList(name=n)
			w.save()
			response.user.watchlist.add(w)
		return HttpResponseRedirect("/%i" %t.id)

	else:
		form = CreateNewList()
	return render(response, "main/create.html", {"form":form})

def view(response):
	return render(response, "main/view.html", {}) 

def add_watchlist(request):
	user = request.user
	if request.method == 'POST':
		watchlist_id = request.POST.get('watchlist_id')
		watchlist_obj = Post.object.get(id=watchlist_id)

		if user in watchlist_obj.liked.all():
			watchlist.obj.remove(user)
		else:
			post_obj.liked.add
	return redirect('watchlist:stock-list')
