from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from hmeteo.models import HTheItem
from hmeteo.forms import HObjForm

# CRUD
# GET : retrieve, list
# POST create, update, delete

@login_required(login_url='/login')
def create(request):
    template='hmeteo/create.html'
    form = HObjForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user=request.user
        obj.save()
        return redirect("/hmeteo")
    else:
        print(form.errors)
    context ={"title":'Location Create', "form": form}
    return render(request,template, context)


def list(request):
#    now=timezone.now()
    if (request.user.is_staff):
        queryset=HTheItem.objects.all()
    else:
        queryset=HTheItem.objects.all().published()
    template='hmeteo/list.html'
    context ={"title":'All Meteos', "object_list": queryset}
    return render(request,template, context)


def detail(request,slug_id):
    pobj = get_object_or_404(HTheItem,slug=slug_id)
    context ={"title":'Location', "item": pobj}
    template="hmeteo/view.html"
    return render(request,template, context)

@login_required(login_url='/login')
def update(request,slug_id):
    pobj = get_object_or_404(HTheItem,slug=slug_id)
    form= HObjForm(request.POST or None, request.FILES or None,instance=pobj)
    print(request.POST)
    print(request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/hmeteo")
    context ={"title": f'Update {pobj.location}', "form": form}
    template="hmeteo/update.html"
    return render(request,template, context)

@login_required(login_url='/login')
def delete(request,slug_id):
    pobj = get_object_or_404(HTheItem,slug=slug_id)
    if request.method == 'POST':
        pobj.delete()
        return redirect("/hmeteo")
    context ={"title":'Location Delete', "item": pobj}
    template="hmeteo/delete.html"
    return render(request,template, context)

 