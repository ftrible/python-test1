from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BookItem, Author
from .forms import BookForm, AuthorForm

# CRUD
# GET : retrieve, list
# POST create, update, delete

@login_required(login_url='/login')
def create(request):
    template='book/create.html'
    # print(request.POST)
    # request.user exists because of the decorator
    form = BookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user=request.user
        obj.slug = BookForm.generate_unique_slug(obj.title)
        obj.save()
        #reset form
        form=BookForm()
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
    context ={"title":'Book', "book": pobj}
    template="book/view.html"
    return render(request,template, context)

@login_required(login_url='/login')
def update(request,slug_id):
    pobj = get_object_or_404(BookItem,slug=slug_id)
    form= BookForm(request.POST or None, request.FILES or None,instance=pobj)
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
    context ={"title":'Book Delete', "book": pobj}
    template="book/delete.html"
    return render(request,template, context)

def author_list(request):
    authors = Author.objects.all()
    return render(request, "book/author_list.html", {"authors": authors})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, "book/author_detail.html", {"author": author})

def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm()
    return render(request, "book/author_form.html", {"form": form})

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect("author_detail", pk=pk)
    else:
        form = AuthorForm(instance=author)
    return render(request, "book/author_form.html", {"form": form})

def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect("author_list")
    return render(request, "book/author_confirm_delete.html", {"author": author})

