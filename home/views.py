from django.shortcuts import render

import geocoder

# Create your views here.

# index
def index(request):
    latlng = geocoder.ip('me')
    # if request.user.is_authenticated: 
    #     print(request.user,'User already logged in')
    #     return render(request,'admin/dashboard.html')
    # else:
    print(latlng)
    print(latlng.ip)
    print(latlng.lat)
    print(latlng.lng)
    # return render(request,'index.html',{'lat':latlng.lat, 'lng':latlng.lng})
    return render(request,'home/index.html',{'lat':9.617436 ,'lng': 76.532735})


def donation(request):
    return render(request,'home/donation.html')
