from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BookItem
from .forms import ObjForm

# CRUD
# GET : retrieve, list
# POST create, update, delete

@login_required(login_url='/login')
def create(request):
    template='book/create.html'
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
    context ={"title":'Book Create', "form": form}
    return render(request,template, context)


def list(request):
#    now=timezone.now()
    if (request.user.is_staff):
        queryset=BookItem.objects.all()
    else:
        queryset=BookItem.objects.all().published()
    template='book/list.html'
    context ={"title":'All Books', "object_list": queryset}
    return render(request,template, context)


def detail(request,slug_id):
    pobj = get_object_or_404(BookItem,slug=slug_id)
    context ={"title":'Book', "post": pobj}
    template="book/view.html"
    return render(request,template, context)

@login_required(login_url='/login')
def update(request,slug_id):
    pobj = get_object_or_404(BookItem,slug=slug_id)
    form= ObjForm(request.POST or None, request.FILES or None,instance=pobj)
    print(request.POST)
    print(request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/book")
    context ={"title": f'Update {pobj.title}', "form": form}
    template="book/update.html"
    return render(request,template, context)

@login_required(login_url='/login')
def delete(request,slug_id):
    pobj = get_object_or_404(BookItem,slug=slug_id)
    if request.method == 'POST':
        pobj.delete()
        return redirect("/book")
    context ={"title":'Book Delete', "post": pobj}
    template="book/delete.html"
    return render(request,template, context)

 