from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def homeview(request):
    # default values
    parameters = {'latitude':37.7749, 'longitude':-122.4194, 'stateName':'Unknown'}

    if request.method == "POST":
        print(request.POST.get("latitude"))
        print(request.POST.get("longitude"))
        print(request.POST.get("stateName"))
        request.session['latitude'] = request.POST.get("latitude")
        request.session['longitude'] = request.POST.get("longitude")
        request.session['stateName'] = request.POST.get("stateName")
        if request.session['stateName'] != "Unknown":
            return redirect('estimate/')
            #return estimateview(request)

    if 'latitude' in request.session and 'longitude' in request.session and 'stateName' in request.session:
        parameters = {'latitude':request.session['latitude'], 'longitude':request.session['longitude'], 'stateName':request.session['stateName']} 
    
    return render(request, 'home.html', parameters)

def estimateview(request):
    return render(request, 'estimate.html', {})