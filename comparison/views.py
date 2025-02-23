from django.shortcuts import render
from solar.data import SOLAR_COST_PER_M2
from stats.data import ELECTRICITY_COST
import json

def compare_elec_trad(request):
    state = request.session.get('state', 'Wisconsin')
    years = list(range(2024, 2044))  # 20 years
    base_electricity_cost = get_state_value(state, ELECTRICITY_COST)*(10500/12)  # Starting electricity cost per kWh

    # Compute cumulative electricity costs (each year's cost adds up)
    electricity_costs = []
    total_electricity_cost = 0  
    for i in range(len(years)):
        yearly_cost = base_electricity_cost * (1.04 ** i)  # Increase by 4% annually
        total_electricity_cost += yearly_cost
        electricity_costs.append(round(total_electricity_cost, 4))  

    # Handle user inputs for solar installation and panel area
    try:
        original_solar_cost = float(request.GET.get('solar_cost', 500))  # Default: $500
        panel_area = float(request.GET.get('panel_area', 100))  # Default: 100 sqft
    except ValueError:
        original_solar_cost = 500
        panel_area = 100

    # Apply 30% tax reduction to solar installation cost
    reduced_solar_cost = original_solar_cost * 0.7  

    # Maintenance cost calculation
    maintenance_cost_per_sqft =  get_state_value(state, SOLAR_COST_PER_M2) 
    maintenance_costs = [panel_area * maintenance_cost_per_sqft] * len(years)

    return render(request, 'chart.html', {
        'years': json.dumps(years),
        'electricity_costs': json.dumps(electricity_costs),  
        'original_solar_cost': original_solar_cost,  # Send original cost
        'reduced_solar_cost': reduced_solar_cost,  # Send reduced cost
        'maintenance_costs': json.dumps(maintenance_costs),  
        'panel_area': panel_area  
    })
    
def get_state_value(state_name, dict):
    return dict.get(state_name, 100)
