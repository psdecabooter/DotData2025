from django.shortcuts import render, redirect
from django.http import HttpResponse
from solar.utils.api_client import get_ghi
from rex import Resource

from solar.data import SOLAR_COST_PER_M2
from stats.data import ELECTRICITY_COST

# Create your views here.
def homeview(request):
    # default values
    parameters = {'latitude':37.7749, 'longitude':-122.4194, 'stateName':'Unknown'}

    if request.method == "POST":
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
    # default values
    parameters = {'latitude':37.7749, 'longitude':-122.4194, 'stateName':'Wisconsin', 'calculations':[]}
    parameters['pricePer'] = SOLAR_COST_PER_M2.get(parameters['stateName'])
    if 'latitude' in request.session and 'longitude' in request.session and 'stateName' in request.session:
        parameters['latitude'] = request.session['latitude']
        parameters['longitude'] = request.session['longitude']
        parameters['stateName'] = request.session['stateName']
        parameters['pricePer'] = SOLAR_COST_PER_M2.get(parameters['stateName'])
    
    if request.method == "POST":
        request.session['efficiency'] = request.POST.get("efficiency") if request.POST.get("efficiency") != '' else 20
        request.session['size'] = request.POST.get("size") if request.POST.get("efficiency") != '' else 50
        request.session['pricePer'] = request.POST.get("pricePer") if request.POST.get("pricePer") != '' else SOLAR_COST_PER_M2.get(parameters['stateName'])

        ghi_value = get_ghi(float(request.session['latitude']), float(request.session['longitude']))

        # CREATING THE TABLE OF INFORMATION
        # Calculate estimated power output (Watts)
        power_output = ghi_value * (float(request.session['efficiency']) / 100) * float(request.session['size'])

        parameters['calculations'].append({
            'ghi': ghi_value,
            'efficiency': float(request.session['efficiency']),
            'size': float(request.session['size']),
            "power_output": round(power_output, 2),
            "initial_investment": float(request.session['size']) * float(request.session['pricePer'])
        })

    return render(request, 'estimate.html', parameters)