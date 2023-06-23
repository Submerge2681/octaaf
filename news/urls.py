from django.urls import path
from .import views

urlpatterns = [
    path('',views.home),
    path('NAT',views.home),
    path('INT',views.home),
    path('LOC',views.home)
]