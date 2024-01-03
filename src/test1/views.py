from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
#from django.utils import timezone
from .models import BlogPost
from .forms import BlogForm

# Create your views here.
def home_page(request):
    context ={"title":'Home'}
    template="home.html"
    queryset=BlogPost.objects.all().published()
    context ={"object_list": queryset[:2]}
    return render(request,template, context)

def contact_page(request):
    context ={"title":'Contact'}
    template="contact.html"
    return render(request,template, context)

def about_page(request):
    context ={"title":'About'}
    template="about.html"
    return render(request,template, context)

# CRUD
# GET : retrieve, list
# POST create, update, delete

@login_required(login_url='/login')
def blog_create(request):
    template='blog/create.html'
    # print(request.POST)
    # request.user exists because of the decorator
    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user=request.user
        obj.save()
        #reset form
        form=BlogForm()
    else:
        print(form.errors)
    context ={"title":'Blog Create', "form": form}
    return render(request,template, context)


def blog_list(request):
#    now=timezone.now()
    if (request.user.is_staff):
        queryset=BlogPost.objects.all()
    else:
        queryset=BlogPost.objects.all().published()
#    queryset=BlogPost.objects.filter(publish_date__gte=now)
    template='blog/list.html'
    context ={"title":'All Posts', "object_list": queryset}
    return render(request,template, context)


def blog_detail(request,slug_id):
    queryset=BlogPost.objects.filter(slug=slug_id)
    if queryset.count == 0:
        raise Http404
    pobj=queryset.first()
    context ={"title":'Blog', "post": pobj}
    template="blog/view.html"
    return render(request,template, context)

@login_required(login_url='/login')
def blog_update(request,slug_id):
    queryset=BlogPost.objects.filter(slug=slug_id)
    if queryset.count == 0:
        raise Http404
    pobj=queryset.first()
    form= BlogForm(request.POST or None, request.FILES or None,instance=pobj)
    print(request.POST)
    print(request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/blog")
    context ={"title": f'Update {pobj.title}', "form": form}
    template="blog/update.html"
    return render(request,template, context)

@login_required(login_url='/login')
def blog_delete(request,slug_id):
    queryset=BlogPost.objects.filter(slug=slug_id)
    if queryset.count == 0:
        raise Http404
    pobj=queryset.first()
    if request.method == 'POST':
        pobj.delete()
        return redirect("/blog")
    context ={"title":'Blog Delete', "post": pobj}
    template="blog/delete.html"
    return render(request,template, context)

from django.shortcuts import render, redirect                                
from django.contrib.auth import authenticate, login                          
from .forms import LoginForm                                                 
                                                                                
def login_view(request):                                                     
    if request.method == 'POST':                                             
        form = LoginForm(request.POST)                 
        if form.is_valid():  
            print(form.cleaned_data)                                                   
            username = form.cleaned_data.get('username')                     
            password = form.cleaned_data.get('password')                     
            user = authenticate(username=username, password=password)  
            print(user)      
            if user is not None:                                             
                login(request, user)                                         
                return redirect('home') 
            else:                                                            
                form.add_error(None, "Invalid username or password")                                     
    else:                                                                    
        form = LoginForm()                                                   
    return render(request, 'login.html', {'form': form}) 