from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homeview, name="home"),
    path('estimate/', views.estimateview, name="estimate")
]