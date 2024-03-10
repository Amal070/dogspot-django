from django.shortcuts import render, redirect

import geocoder

from user.models import Map_Details
from user.models import missing_case
from user.models import comment
from user.models import missing_report
from user.models import adoption,adoption_request
from accounts.models import User
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

    map_db = Map_Details.objects.all()
    return render(request,'home/home.html',{'lat':latlng.lat, 'lng':latlng.lng, 'map_db': map_db})



# map for listing all dog spots
def map(request):
    latlng = geocoder.ip('me')

    map_db = Map_Details.objects.all()
    context = {'map_db': map_db, 'lat':latlng.lat, 'lng':latlng.lng}
    return render(request, 'home/map.html', context)

def dogspot_list(request,pk):
    map_data = Map_Details.objects.get(pk=pk)
    # print(map_data, request.user.role)
    context = {'map_data' : map_data }
    return render(request, 'home/dogspot_list.html', context)


def donation(request):
    context = {}
    return render(request, 'home/donation.html', context)


def missing_cases(request):
    missing=missing_case.objects.all()

    return render(request,'home/missing_case.html',{'missing':missing})

def missing_details(request,pk):
    
    missing=missing_case.objects.get(pk=pk)
    comm=comment.objects.filter(missing_id=pk)
    if request.POST:
        commenter=request.POST.get('Comments')
        comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk),user_id=User.objects.get(pk=request.user.id))
        comment_obj.save()
    return render(request,'home/missing_details.html',{'missing':missing,'comm':comm})



def comment_delete(request,pk):

    com_dele=comment.objects.get(id=pk)
    com_dele.delete()
    return redirect('/missing_details/' + str(com_dele.missing_id_id))


def missing_rpt(request,pk):
    if request.POST:
        category=request.POST.get('category')
        summery=request.POST.get('summery')
        report_obj=missing_report(category=category,report_summery=summery,user_id=User.objects.get(id=request.user.id),missing_id=missing_case.objects.get(pk=pk))
        report_obj.save()
    return render(request,'home/missing_report.html')


def adoption_view(request):
    
    adoption1=adoption.objects.all()
    return render(request,'home/adoption.html',{'adoption': adoption1})

def adoption_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    adoption_req=adoption_request.objects.filter(user_id=request.user.id,adoption_id=pk,approval_request='accept').first()
    if request.POST:
        if not adoption_request.objects.filter(user_id=request.user.id,adoption_id=pk).exists():
            adoption_req=adoption_request(user_id=User.objects.get(id=request.user.id), adoption_id=pk,approval_request='accept')
            adoption_req.save()
    return render(request,'home/adoption_details.html',{'adoption2':adoption2,'adoption_req':adoption_req})

