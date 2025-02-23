from django.urls import path
from . import views

urlpatterns = [
     path('radiation/', views.ghi_view),
]

