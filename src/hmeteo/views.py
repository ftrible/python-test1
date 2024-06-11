from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from hmeteo.models import HTheItem
from django.views.decorators.csrf import csrf_exempt
from hmeteo.forms import HObjForm
from django.http import JsonResponse
# https://opencagedata.com/dashboard#geocoding
# See full Python tutorial:
# https://opencagedata.com/tutorials/geocode-in-python
from opencage.geocoder import OpenCageGeocode
import json

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
def createwithobject(request):
    if request.method == 'POST':
        form = HObjForm(request.POST, request.FILES)
        if form.is_valid():
            # Retrieve the additional JSON data from the request.POST
            location_geo = request.POST.get('location_geo')
            if location_geo:
                location_geo = json.loads(location_geo)  # Parse the JSON string
                # Manually set the form instance fields using location_geo data
                obj = form.save(commit=False)
                obj.user = request.user
                obj.lat = location_geo['geometry']['lat']
                obj.lng = location_geo['geometry']['lng']
                obj.location = location_geo['formatted']
                obj.slug = HObjForm.generate_unique_slug(location_name=location_geo['formatted'])
                obj.save()
                # Return a JsonResponse or HttpResponse as needed
                return JsonResponse({'message': 'Location created successfully'}, status=200)

            else:
                return JsonResponse({'error': 'location_geo not provided'}, status=400)
        else:
            return JsonResponse({'error': form.errors}, status=400)

    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
def geocode(request):
    print("********* Geocode ************")
    json_data=request.body.decode('utf-8')
    print( json_data)
    data_dict = json.loads(json_data)
    location_name = data_dict.get('location_name')
    print(location_name)
    OCG = OpenCageGeocode('e3dd0f92c031405abba83cfeefbacd4e')
    results = OCG.geocode(location_name)
    for town in results:
        print(town['components']['country'])
    return JsonResponse(results, safe=False)

def list(request):
#    now=timezone.now()
    queryset=HTheItem.objects.all()
    template='hmeteo/list.html'
    context ={"title":'All Locations', "object_list": queryset}
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

@csrf_exempt
def update_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('id')
        new_location = data.get('new_location')
        # Update the database
        try:
            item = HTheItem.objects.get(id=item_id)
            item.location = new_location
            item.save()
            return JsonResponse({'success': True})
        except HTheItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

 