from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TheItem
from hmeteo.models import MeteoItem
from book.models import BookItem
from .forms import ObjForm

# Create your views here.
def home_page(request):
    context ={"title":'Home'}
    template="home.html"
    blqueryset=TheItem.objects.all().published()
    boqueryset=BookItem.objects.all()
    hqueryset=MeteoItem.objects.all()
    context ={"object_list": blqueryset[:2], "meteo_list": hqueryset[:2], "book_list": boqueryset[:2]}
    return render(request,template, context)

# CRUD
# GET : retrieve, list
# POST create, update, delete

@login_required(login_url='/login')
def create(request):
    template='blog/create.html'
    # print(request.POST)
    # request.user exists because of the decorator
    form = ObjForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user=request.user
        obj.save()
        #reset form
        form=ObjForm()
    else:
        print(form.errors)
    context ={"title":'Blog Create', "form": form}
    return render(request,template, context)


def list(request):
#    now=timezone.now()
    if (request.user.is_staff):
        queryset=TheItem.objects.all()
    else:
        queryset=TheItem.objects.all().published()
    template='blog/list.html'
    context ={"title":'All Posts', "object_list": queryset}
    return render(request,template, context)


def detail(request,slug_id):
    pobj = get_object_or_404(TheItem,slug=slug_id)
    context ={"title":'Blog', "post": pobj}
    template="blog/view.html"
    return render(request,template, context)

@login_required(login_url='/login')
def update(request,slug_id):
    pobj = get_object_or_404(TheItem,slug=slug_id)
    form= ObjForm(request.POST or None, request.FILES or None,instance=pobj)
    print(request.POST)
    print(request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/blog")
    context ={"title": f'Update {pobj.title}', "form": form}
    template="blog/update.html"
    return render(request,template, context)

@login_required(login_url='/login')
def delete(request,slug_id):
    pobj = get_object_or_404(TheItem,slug=slug_id)
    if request.method == 'POST':
        pobj.delete()
        return redirect("/blog")
    context ={"title":'Blog Delete', "post": pobj}
    template="blog/delete.html"
    return render(request,template, context)

 