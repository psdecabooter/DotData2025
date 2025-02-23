from django.shortcuts import render
from solar.data import SOLAR_COST_PER_M2
from stats.data import ELECTRICITY_COST
import json

def use_state(request):
    return request.session.get('state', 'Wisconsin')

def compare_elec_trad(request):
    state = use_state(request)
    years = list(range(2024, 2044))  # 20 years
    base_electricity_cost = (ELECTRICITY_COST.get(state))*(10500/100)  # Starting electricity cost per kWh

    # Compute cumulative electricity costs (each year's cost adds up)
    electricity_costs = []
    total_electricity_cost = 0  
    for i in range(len(years)):
        yearly_cost = base_electricity_cost * (1.04 ** i)  # Increase by 4% annually
        electricity_costs.append(round(yearly_cost, 4))  

    # Handle user inputs for solar installation and panel area
    try:
        panel_area = float(request.session.get('size'))  # Default: 100 m^2
    except ValueError:
        panel_area = 5

    original_solar_cost = panel_area * SOLAR_COST_PER_M2.get(state)  # Calculate solar installation cost
    # Apply 30% tax reduction to solar installation cost
    reduced_solar_cost = original_solar_cost * 0.7  

    # Maintenance cost calculation
    maintenance_costs = [300]

    return render(request, 'chart.html', {
        'years': json.dumps(years),
        'electricity_costs': json.dumps(electricity_costs),  
        'original_solar_cost': original_solar_cost,  # Send original cost
        'reduced_solar_cost': reduced_solar_cost,  # Send reduced cost
        'maintenance_costs': json.dumps(maintenance_costs),  
        'size': panel_area,
        'state': state
    })
