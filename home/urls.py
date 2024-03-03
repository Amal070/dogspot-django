from django.urls import path

from home.views import *



urlpatterns = [
    path('', index, name='home.index'),
    path('donation/', donation, name='home.donation'),


]