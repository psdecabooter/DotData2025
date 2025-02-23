from django.shortcuts import render, redirect
from django.http import HttpResponse
from solar.utils.api_client import get_ghi
from rex import Resource

from solar.data import SOLAR_COST_PER_M2
from stats.data import ELECTRICITY_COST
import json

# Create your views here.
def homeview(request):
    # default values
    parameters = {'latitude':37.7749, 'longitude':-122.4194, 'stateName':'Unknown'}

    if request.method == "POST":
        request.session['latitude'] = request.POST.get("latitude")
        request.session['longitude'] = request.POST.get("longitude")
        request.session['stateName'] = request.POST.get("stateName")
        request.session['newLocation'] = True
        if request.session['stateName'] != "Unknown":
            return redirect('estimate/')

    if 'latitude' in request.session and 'longitude' in request.session and 'stateName' in request.session:
        parameters = {'latitude':request.session['latitude'], 'longitude':request.session['longitude'], 'stateName':request.session['stateName']} 
    
    return render(request, 'home.html', parameters)

def estimateview(request):
    # default values
    parameters = {'latitude':37.7749, 'longitude':-122.4194, 'stateName':'Wisconsin', 'calculations':[]}
    parameters['statePrice'] = SOLAR_COST_PER_M2.get(parameters['stateName'])
    if 'latitude' in request.session and 'longitude' in request.session and 'stateName' in request.session:
        parameters['latitude'] = request.session['latitude']
        parameters['longitude'] = request.session['longitude']
        parameters['stateName'] = request.session['stateName']
        parameters['statePrice'] = SOLAR_COST_PER_M2.get(parameters['stateName'])
    
    if request.method == "POST":
        #check if the user changed the location
        sameLongLat = False
        if 'newLocation' in request.session:
            sameLongLat = not request.session['newLocation']
        request.session['newLocation'] = False
        request.session['efficiency'] = request.POST.get("efficiency") if request.POST.get("efficiency") != '' else 20
        parameters['efficiency'] = request.session['efficiency']
        request.session['size'] = request.POST.get("size") if request.POST.get("size") != '' else 50
        parameters['size'] = request.session['size']
        request.session['pricePer'] = request.POST.get("pricePer") if request.POST.get("pricePer") != '' else SOLAR_COST_PER_M2.get(parameters['stateName'])
        parameters['pricePer'] = request.session['pricePer']


        ghi_value = 0
        if sameLongLat and 'ghi' in request.session:
            ghi_value = request.session['ghi']
            print("FAST")
            print(sameLongLat)
        else:
            ghi_value = get_ghi(float(request.session['latitude']), float(request.session['longitude']))
            request.session['ghi'] = ghi_value

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

        # CREATING THE GRAPH
        state = request.session['stateName']
        years = list(range(2024, 2044))  # 20 years
        base_electricity_cost = (ELECTRICITY_COST.get(state))*(10500/100)  # Starting electricity cost per kWh
        original_solar_cost = float(request.session['size']) * float(request.session['pricePer'])
        # Reduction from solar credit
        reduced_solar_cost = original_solar_cost * 0.7  

        # Compute cumulative electricity costs (each year's cost adds up)
        electricity_costs = []
        total_electricity_cost = 0  
        for i in range(len(years)):
            yearly_cost = base_electricity_cost * (1.04 ** i)  # Increase by 4% annually
            electricity_costs.append(round(yearly_cost, 4))  
        
        # Maintenance cost calculation
        maintenance_costs = [300]

        parameters['chart'] = {
            'years': json.dumps(years),
            'electricity_costs': json.dumps(electricity_costs),  
            'original_solar_cost': original_solar_cost,  # Send original cost
            'reduced_solar_cost': reduced_solar_cost,  # Send reduced cost
            'maintenance_costs': json.dumps(maintenance_costs),  
            'size': float(request.session['size']),
            'state': request.session['stateName']
        }        

    return render(request, 'estimate.html', parameters)