from django.urls import path
from .views import compare_elec_trad

urlpatterns = [
    path('chart/', compare_elec_trad, name='electricity_vs_solar'),
]