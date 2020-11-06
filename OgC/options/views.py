from django.shortcuts import render
from django.views.generic import TemplateView, ListView
#from .forms import SearchForm
from .models import Option
# Create your views here.

class HomepageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = Option
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = option.objects.filter(
            Q(name__icontains=query) 
        )
        return object_list