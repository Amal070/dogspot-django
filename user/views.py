from django.shortcuts import render, redirect

from user.models import Map_Details, Dog_Pics
from django.contrib import messages

from django.http import JsonResponse
from user.models import missing_case
from user.models import comment
from user.models import missing_report
from user.models import adoption,adoption_request




import geocoder
# Create your views here.

from accounts.models import User

# dashboard
def dashboard(request):
   
    user_count=User.objects.all().count()
    print('user_count:',user_count)
    return render(request, 'user/dashboard.html',{'user_count':user_count})

# show all dogspot marker in map
def map_view(request):
    latlng = geocoder.ip('me')
    # if request.user.is_authenticated: 
    #     print(request.user,'User already logged in')
    #     return render(request,'admin/dashboard.html')
    # else:
    print(latlng)
    print(latlng.ip)
    print(latlng.lat)
    print(latlng.lng)
    return render(request, 'user/map_view.html',{'lat':latlng.lat, 'lng':latlng.lng})


def static_dogspot_marker_map(request):
    latlng = geocoder.ip('me')
    # if request.user.is_authenticated: 
    #     print(request.user,'User already logged in')
    #     return render(request,'admin/dashboard.html')
    # else:
    print(latlng)
    print(latlng.ip)
    print(latlng.lat)
    print(latlng.lng)
    return render(request, 'user/static_dogspot_marker_map.html', {'lat':latlng.lat, 'lng':latlng.lng})


def add_dogspot(request, lat, lng):
    if request.method == 'POST':
        length = request.POST.get('length')
        title = request.POST.get('title')
        description = request.POST.get('description')
        no_of_dogs = request.POST.get('no_of_dogs')
        behaviour = request.POST.get('behaviour')
        # images = request.FILES.getlist('images1')

        print('title', title)
        print('description', description)
        print('no_of_dogs', no_of_dogs)
        print('behaviour', behaviour)
        

        if not Map_Details.objects.filter(latitude=lat,longitude=lng).exists():
            map_obj = Map_Details.objects.create(
                email = request.user.username,
                user = request.user,
                title = title,
                description = description,
                no_of_dogs = no_of_dogs,
                behaviour = behaviour,
                longitude =lng,
                latitude = lat
            )
            print('map details point created successfully')

            for file_num in range(0, int(length)):
                image = request.FILES.get(f'images{file_num}')
                print('image : ', image)
                Dog_Pics.objects.create(
                    map_id = map_obj,
                    image = image
                )
                print('image db created created')

        else:
            # messages.error(request, 'Map Location already added by other user', extra_tags='map_point_already_exist_error')
            print('Map Location already added by other user')
            return JsonResponse({'point_exist': True},safe=False)

    print(request.user, 'usertttttttttttt')

    return render(request, 'user/add_dogspot.html', {'lat':lat, 'lng':lng})

def dogspot_details(request):
    return render(request, 'user/dogspot_details.html')

# update
# delete

# def all_dogspot_list(request):
#     return render(request, 'user/all_dogspot_list.html')


# def profile(request):
#     return render(request, 'user/profile.html')

# def profile_update(request):
#     return render(request, 'user/profile_update.html')


def settings(request):
    return render(request, 'user/profile.html')

def missings_form(request):
    # missings=missing_case(place='kottayam',phone_no=7373773737,description='wanted')
    # missings.save()
    if request.POST:
        dog_name=request.POST.get('dog_name')
        owner_name=request.POST.get('owner_name')
        place=request.POST.get('Place')
        breed=request.POST.get('breed')
        color=request.POST.get('color')
        phone_no=request.POST.get('Phone_no')
        description=request.POST.get('Description')
        image=request.FILES['Image']
        missing_obj=missing_case(place=place,phone_no=phone_no,description=description,image=image,dog_name=dog_name,owner_name=owner_name,breed=breed,color=color,user_id=User.objects.get(id=request.user.id))
        missing_obj.save()
        messages.success(request, 'missing case')
    return render(request,'user/missing_form.html')


def missings(request):
    
    missing=missing_case.objects.filter(user_id=request.user.id)
    return render(request,'user/missing_case.html',{'missing':missing})

def missing_details(request,pk):
    
    missing=missing_case.objects.get(pk=pk)
    return render(request,'user/missing_details.html',{'missing':missing})


def edit(request,pk):
    edit_missing=missing_case.objects.get(pk=pk,user_id=request.user.id)
    if request.POST:
        # edit_missing=missing_case.objects.get(pk=pk)
        dog_name=request.POST.get('dog_name')
        owner_name=request.POST.get('owner_name')
        place=request.POST.get('Place')
        phone_no=request.POST.get('Phone_no')
        breed=request.POST.get('breed')
        color=request.POST.get('color')
        description=request.POST.get('Description')
        image=request.FILES['Image']
        # status=request.POST.get('Status')
        print(place,phone_no,description)
        edit_missing.dog_name=dog_name
        edit_missing.owner_name=owner_name
        edit_missing.place=place
        edit_missing.phone_no=phone_no
        edit_missing.breed=breed
        edit_missing.color=color
        edit_missing.description=description
        edit_missing.image=image
        # edit_missing.status=status
        edit_missing.save()
        messages.success(request, 'missing case')
    return render(request,'user/missing_edit.html',{'edit_missing':edit_missing})


def delete(request,pk):
    missing_delete=missing_case.objects.get(pk=pk)
    missing_delete.delete()
    return redirect(missings)



def comment_view(request,pk):
    if request.POST:
        commenter=request.POST.get('Comments')
        comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk),user_id=User.objects.get(pk=request.user.id))
        comment_obj.save()
    comm=comment.objects.filter(missing_id=pk)
    return render(request,'user/comments.html',{'comm':comm})


def comment_delete(request,pk):

    com_dele=comment.objects.get(id=pk)
    com_dele.delete()
    return redirect('/user/comment/' + str(com_dele.missing_id_id))



def missing_rpt(request,pk):
    if request.POST:
        category=request.POST.get('category')
        summery=request.POST.get('summery')
        report_obj=missing_report(category=category,report_summery=summery,user_id=User.objects.get(id=request.user.id),missing_id=missing_case.objects.get(pk=pk))
        report_obj.save()
    return render(request,'user/missing_report.html')

def report_case(request,pk):
    mis=missing_report.objects.filter(missing_id=pk)
    return render(request,'user/missing_rpt_list.html',{'mis':mis})


def report_list(request):
    li=missing_report.objects.filter(user_id=request.user.id)
    return render(request,'user/report_list.html',{'li':li})


def report_delete(request,pk):
    dele=missing_report.objects.filter(user_id=request.user.id,id=pk)
    dele.delete()
    return redirect(report_list)

def profile(request):
    pro=User.objects.get(id=request.user.id)
    return render(request,'user/profile.html',{'pro':pro})

def profile_edit(request):
    pro_edit=User.objects.get(id=request.user.id)
    if request.POST:
        image=request.FILES['Photo']
        first_name=request.POST.get('First_name')
        last_name=request.POST.get('Last_name')
        place=request.POST.get('Place')
        pro_edit.profile_pic=image
        pro_edit.first_name=first_name
        pro_edit.last_name=last_name
        pro_edit.place=place
        pro_edit.save()
        messages.success(request, 'profile')
    return render(request,'user/profile_update.html',{'pro_edit':pro_edit})



def adoption_form(request):
   
    if request.POST:
        dog_name=request.POST.get('dog_name')
        owner_name=request.POST.get('owner_name')
        address=request.POST.get('Address')
        breed=request.POST.get('breed')
        color=request.POST.get('color')
        phone_no=request.POST.get('Phone_no')
        description=request.POST.get('Description')
        image=request.FILES['Image']
        adoption_obj=adoption(address=address,phone_no=phone_no,description=description,image=image,dog_name=dog_name,owner_name=owner_name,breed=breed,color=color,user_id=User.objects.get(id=request.user.id))
        adoption_obj.save()
        willing_list=User.objects.filter(willing_to_adopt='yes').exclude(id=request.user.id)
        print("willing_list:",willing_list)
        for row in willing_list:
          print(row.first_name,row.id)
          adoption_req=adoption_request(user_id=User.objects.get(id=row.id), adoption_id=adoption_obj.id)
          adoption_req.save()
        messages.success(request, 'adoption')
    return render(request,'user/adoption_form.html')


def adoption_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'user/adoption.html',{'adoption': adoption1})


def edit_adoption(request,pk):
    edit_ad=adoption.objects.get(pk=pk,user_id=request.user.id)
    if request.POST:
        # edit_missing=missing_case.objects.get(pk=pk)
        dog_name=request.POST.get('dog_name')
        owner_name=request.POST.get('owner_name')
        address=request.POST.get('Address')
        phone_no=request.POST.get('Phone_no')
        breed=request.POST.get('breed')
        color=request.POST.get('color')
        description=request.POST.get('Description')
        image=request.FILES['Image']
        # status=request.POST.get('Status')
        # print(address,phone_no,description)
        edit_ad.dog_name=dog_name
        edit_ad.owner_name=owner_name
        edit_ad.address=address
        edit_ad.phone_no=phone_no
        edit_ad.breed=breed
        edit_ad.color=color
        edit_ad.description=description
        edit_ad.image=image
        # edit_missing.status=status
        edit_ad.save()
        messages.success(request, 'adoption')
    return render(request,'user/adoption_edit.html',{'edit_ad':edit_ad})


def adoption_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'user/adoption_details.html',{'adoption2':adoption2})


def adoption_delete(request,pk):
    ad_delete=adoption.objects.get(pk=pk)
    ad_delete.delete()
    return redirect(adoption_view)


def adoption_snd_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'user/adoption_req_snd.html',{'adoption': adoption1})


def adoption_snd_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'user/adoption_snd_details.html',{'adoption2':adoption2})


def request_list(request,pk):
    adoption1=adoption.objects.get(id=pk)
    ruq=adoption_request.objects.filter(adoption_id=pk)
    return render(request, 'user/request_list.html',{'ruq':ruq,'adoption1':adoption1})

def request_profile(request,pk):
    pro=User.objects.get(id=pk)
    return render(request,'user/request_profile.html',{'pro':pro})

def request_cancel(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='cancel'
    ruq.save()
    return redirect('/user/adp_request_list/' + str(ruq.adoption_id))

def request_send(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='active'
    ruq.save()
    return redirect('/user/adp_request_list/' + str(ruq.adoption_id))

def received_list(request):
    ruq=adoption_request.objects.filter(user_id=request.user.id).exclude(approval_request='cancel')
    print("req:",ruq)
    return render(request, 'user/received_list.html',{'ruq':ruq})

def request_accept(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='accept'
    ruq.save()
    return redirect(received_list)

def request_reject(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='reject'
    ruq.save()
    return redirect(received_list)

def recived_cancel(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='active'
    ruq.save()
    return redirect(received_list)

    






    

     







    


        

   


