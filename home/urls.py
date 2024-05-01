from django.urls import path

from home.views import *

urlpatterns = [
    path('', index, name='home.index'),
    path('map/', map, name='home.map'),
    path('dogspot_list/<pk>/', dogspot_list, name='home.dogspot_list'),
    path('donation/', donation, name='home.donation'),
    path('dogspot_rpt/<pk>', dogspot_rpt, name='home.dogspot_rpt'),
    path('missing_case/', missing_cases, name='home.missing_cases'),
    path('missing_details/<pk>', missing_details, name='home.missing_details'),
    path('comment_delete/<pk>', comment_delete, name='home.comment_delete'),
    path('missing_rpt/<pk>', missing_rpt, name='home.missing_rpt'),
    path('adoption_view/', adoption_view, name='home.adoption_view'),
    path('adoption_details/<pk>', adoption_details, name='home.adoption_details'),
]