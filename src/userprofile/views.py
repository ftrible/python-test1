from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from userprofile.models import UserProfile
from userprofile.forms import UserProfileForm
# Create your views here.

@login_required(login_url='/login')
def update(request):
    if not hasattr(request.user, 'userprofile'):
        print('create profile')
        pobj=UserProfile.objects.create(user=request.user)
    else:
        pobj = request.user.userprofile
    print(pobj)
    form= UserProfileForm(request.POST or None, request.FILES or None,instance=pobj)
    print(request.POST)
    print(request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/userprofile")
    context ={"title": f'Update {request.user}', "form": form}
    template="userprofile/update.html"
    return render(request,template, context)