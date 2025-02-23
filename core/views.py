from django.shortcuts import render

# Create your views here.
def homeview(request):
    return render(request, 'home.html', {})

def estimateview(request):
    return render(request, 'estimate.html', {})