from django.shortcuts import render

# Create your views here.
from .models import SearchQuery
from book.models import BookItem
from hmeteo.models import MeteoItem

def search_view(request):
    query=request.GET.get('q', None)
    user=None
    if request.user.is_authenticated:
        user=request.user
    context={"query": query}
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        book_list=BookItem.objects.search(query=query)
        context['book_list']=book_list
        meteo_list=MeteoItem.objects.search(query=query)
        context['meteo_list']= meteo_list
    template='searches/view.html'
    return render(request, template,context)