from django.shortcuts import render
from solar.utils.api_client import get_ghi
from rex import Resource
from django.shortcuts import render, redirect

nsrdb_file = '/nrel/nsrdb/conus/nsrdb_conus_2022.h5'

def solar_estimate(request):
    if request.method == "POST":
        request.session['state'] = request.POST.get('state')  # Store in session
        request.session['latitude'] = request.POST.get('latitude')
        request.session['longitude'] = request.POST.get('longitude')
        request.session['efficiency'] = request.POST.get('efficiency')
        request.session['size'] = request.POST.get('size')
        
        return redirect('comparison:use_state')  # Redirect to another app

    return render(request, 'chart.html')

def ghi_view(request):
    results = []

    if request.method == "POST":
        latitude = float(request.POST.get("latitude"))
        longitude = float(request.POST.get("longitude"))
        efficiency = float(request.POST.get("efficiency"))  # Efficiency as %
        size = float(request.POST.get("size"))  # Panel size in square meters

        ghi_value = get_ghi(latitude, longitude)

        # Calculate estimated power output (Watts)
        power_output = ghi_value * (efficiency / 100) * size

        results.append({
            "latitude": latitude,
            "longitude": longitude,
            "ghi": ghi_value,
            "efficiency": efficiency,
            "size": size,
            "power_output": round(power_output, 2),
        })

    if request.method == "POST":
        state = request.POST.get('state', 'Unknown')  # Get from form, default to 'Unknown'
        request.session['state'] = state
        size = float(request.POST.get('size'))
        request.session['size'] = size

    return render(request, "radiation.html", {"results": results})

def new_page(request):
    return render(request, 'comparison/chart.html')

#we used chatgpt for this file

