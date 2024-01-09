from django.shortcuts import render

# Create your views here.
from .models import SearchQuery
from blog.models import TheItem

def search_view(request):
    query=request.GET.get('q', None)
    user=None
    if request.user.is_authenticated:
        user=request.user
    context={"query": query}
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        blog_list=TheItem.objects.search(query=query)
        context['blog_list']= blog_list
    template='searches/view.html'
    return render(request, template,context)