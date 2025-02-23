from django.shortcuts import render
from solar.utils.api_client import get_ghi
from rex import Resource

nsrdb_file = '/nrel/nsrdb/conus/nsrdb_conus_2022.h5'


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

    return render(request, "radiation.html", {"results": results})

#we used chatgpt for this file

