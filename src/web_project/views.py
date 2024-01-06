from smtplib import SMTPAuthenticationError
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm  

def contact_page(request):
    context ={"title":'Contact'}
    template="contact.html"
    return render(request,template, context)

def about_page(request):
    context ={"title":'About'}
    template="about.html"
    return render(request,template, context)

from django.shortcuts import render, redirect                                
from django.contrib.auth import authenticate, login                          
from .forms import LoginForm                                                 
                                                                                
def login_view(request):                                                     
    if request.method == 'POST':                                    
        form = AuthenticationForm(data=request.POST)   
        if form.is_valid():  
            username = form.cleaned_data.get('username')                     
            password = form.cleaned_data.get('password')  
            user = authenticate(username=username, password=password)  
            if user is not None:                                             
                login(request, user)                                         
                return redirect('home') 
            else:                                                            
                form.add_error(None, "Invalid username or password")  
        else:
            pass # incorrect user                                   
    else:                                                                    
        form = LoginForm()                                                   
    return render(request, 'login.html', {'form': form})


def forgot_password(request):
    
    form = PasswordResetForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
                form.save(request=request) #, email_template_name='path/to/your/email_template.html')
                return redirect('home') 
        else:
            form.add_error(None, "Invalid email") 
    return render(request, 'simple.html', {'form': form})
