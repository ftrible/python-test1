from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BookItem, Author
from .forms import BookForm, AuthorForm
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import os
import json

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
    queryset=BookItem.objects.all()
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

@csrf_exempt  # If you use AJAX with CSRF, you can remove this and use the CSRF token header
@require_POST
def vision_api(request):
    data = json.loads(request.body)
    image_base64 = data.get('image')
    api_key = os.environ.get('GOOGLE_VISION_API_KEY')  # Set your API key as an environment variable

    url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'
    payload = {
        "requests": [{
            "image": {"content": image_base64},
            "features": [{"type": "TEXT_DETECTION"}]
        }]
    }
    response = requests.post(url, json=payload)
    result = response.json()

    # Parse the main detected text
    try:
        annotations = result['responses'][0].get('textAnnotations', [])
        full_text = annotations[0]['description'] if annotations else ''
        # Optionally, get all lines/words as a list:
        lines = [ann['description'] for ann in annotations[1:]] if len(annotations) > 1 else []
    except (KeyError, IndexError):
        full_text = ''
        lines = []

    return JsonResponse({
        'full_text': full_text,
        'lines': lines,
        'raw': result  # Optionally include the raw response for debugging
    })