from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Demandes
from hmeteo.models import MeteoItem
from .forms import DemandesForm

# CRUD
# GET : retrieve, list
# POST create, update, delete

@login_required(login_url='/login')
def create(request):
    template='demandes/create.html'
    # print(request.POST)
    # request.user exists because of the decorator
    form = DemandesForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user=request.user
        obj.save()
        #reset form
        form=DemandesForm()
    else:
        print(form.errors)
    context ={"title":'Demande Create', "form": form}
    return render(request,template, context)


def list(request):
#    now=timezone.now()
    if (request.user.is_staff):
        queryset=Demandes.objects.all()
    else:
        queryset=Demandes.objects.all().published()
    template='demandes/list.html'
    context ={"title":'All Posts', "object_list": queryset}
    return render(request,template, context)


def detail(request,slug_id):
    pobj = get_object_or_404(Demandes,slug=slug_id)
    context ={"title":'Demande', "demande": pobj}
    template="demandes/view.html"
    return render(request,template, context)

@login_required(login_url='/login')
def update(request,slug_id):
    pobj = get_object_or_404(Demandes,slug=slug_id)
    form= Demandes(request.POST or None, request.FILES or None,instance=pobj)
    print(request.POST)
    print(request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/demandes")
    context ={"title": f'Update {pobj.title}', "form": form}
    template="demandes/update.html"
    return render(request,template, context)

@login_required(login_url='/login')
def delete(request,slug_id):
    pobj = get_object_or_404(Demandes,slug=slug_id)
    if request.method == 'POST':
        pobj.delete()
        return redirect("/demandes")
    context ={"title":'Demande Delete', "demande": pobj}
    template="demandes/delete.html"
    return render(request,template, context)

 