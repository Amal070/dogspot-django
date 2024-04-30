from django.shortcuts import render,redirect
from django.http import JsonResponse

from django.contrib import messages

import geocoder
from user.models import missing_case
from user.models import comment
from user.models import missing_report
from accounts.models import User
from user.models import adoption,adoption_request
from django.contrib.auth.decorators import login_required

from user.models import Map_Details, Dog_Pics



# Create your views here.
@login_required
def dashboard(request):
    users_count=User.objects.all().exclude(role='admin').count()
    context = {'users_count' : users_count}
    return render(request, 'admin/dashboard.html', context)

@login_required
def users(request):
    user=User.objects.all()
    return render(request, 'admin/users.html',{'user':user})

@login_required
def user_details(request,pk):
    user=User.objects.get(pk=pk)
    return render(request,'admin/user_details.html',{'user':user})

@login_required
def user_search(request):
    search_key=request.POST.get('search_key')
    # name_parts = search_key.split(' ')
    # print('dffd', name_parts)

    # if len(name_parts) >= 2:
    #     first, last = name_parts
    #     # Now you can use 'first' and 'last' as needed
    #     print('First Name:', first)
    #     print('Last Name:', last)

    search=User.objects.filter(first_name__icontains=search_key)
    return render(request,'admin/users.html',{'user':search})
    

@login_required
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

    map_db = Map_Details.objects.all()
    
    context = {'lat':latlng.lat, 'lng':latlng.lng, 'map_db' : map_db}
    return render(request, 'admin/map_view.html', context)


@login_required
def dogspot_marker_map(request):
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
    context = {'lat':latlng.lat, 'lng':latlng.lng, 'map_db' : map_db}
    return render(request, 'admin/dogspot_marker_map.html', context)


from PIL import Image, ImageFilter # for image compression
from io import BytesIO # for image compression
from django.core.files.base import ContentFile #for image compression
# image compression function
def image_compressor(image_file, quality=90):
    try:
        # Open the image using PIL
        img = Image.open(image_file)
        print(f'image name: {image_file} is compressing.........')

        # Resize the image (optional, if you want to resize)
        width, height = img.size
        # img = img.resize((width, height), Image.ANTIALIAS)
        img = img.resize((width, height), ImageFilter.ANTIALIAS)

        # Convert image to bytes with compression quality
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG', quality=quality)

        # Reset the file pointer to the beginning
        img_bytes.seek(0)

        # Create a ContentFile object from the compressed image data
        compressed_image = ContentFile(img_bytes.read(), name=image_file.name)

        return compressed_image # ready for saving to database in "ImageField" field
    
    except:
        print('image compression failed.....so real image returned for saving')
        return image_file

@login_required
def add_dogspot(request, lat, lng):
    if request.method == 'POST':
        length = request.POST.get('length')
        place_name = request.POST.get('place_name')
        description = request.POST.get('description')
        no_of_dogs = request.POST.get('no_of_dogs')
        behaviour = request.POST.get('behaviour')
        km = request.POST.get('km')
        # images = request.FILES.getlist('images1')

        print('place_name', place_name)
        print('description', description)
        print('no_of_dogs', no_of_dogs)
        print('behaviour', behaviour)
        print('km:', km)

        #  Aggressive, Biting, Social, Friendly, Barking, Chasing, Territorial, Illness 
        zone = {}
        # Red Zone (Aggressive, Biting, Territorial, Illness):
        if 'Aggressive' in behaviour or 'Biting' in behaviour or 'Territorial' in behaviour or 'Illness' in behaviour:
            print( 'Red Zone (Aggressive, Biting, Territorial, Illness):..................')

            zone['zone'] = 'red'
            zone['radius_color'] = '#FF0000'
            zone['radius_color_hexcode'] = '#FF0000'

        # Yellow Zone (Barking, Chasing):
        elif 'Barking' in behaviour or 'Chasing' in behaviour:
            print('Yellow Zone (Barking, Chasing):..................')

            zone['zone'] = 'yellow'
            zone['radius_color'] = '#FFD326'
            zone['radius_color_hexcode'] = '#FFD326'

        # Green Zone (Social, Friendly)
        else:
            print(' Green Zone (Social, Friendly)..................')

            zone['zone'] = 'green'
            zone['radius_color'] = '#2AAD27'
            zone['radius_color_hexcode'] = '#2AAD27'

        print('Zone dictionary:', zone)
        print('Zone:', zone['zone'])
        print('radius_color:', zone['radius_color'])
        print('radius_color_hexcode:', zone['radius_color_hexcode'])
        

        if not Map_Details.objects.filter(latitude=lat,longitude=lng).exists():
            map_obj = Map_Details.objects.create(
                email = request.user.username,
                user = request.user,
                place_name = place_name,
                description = description,
                no_of_dogs = no_of_dogs,
                behaviour = behaviour,
                longitude = lng,
                latitude = lat,
                zone = zone['zone'],
                radius_color=zone['radius_color'],
                radius_color_hexcode=zone['radius_color_hexcode'],
                km_distance=km
            )
            print('map details point created successfully')

            for file_num in range(0, int(length)):
                image = request.FILES.get(f'images{file_num}')
                print('image : ', image)
                Dog_Pics.objects.create(
                    map_id = map_obj,
                    # image = image
                    image = image_compressor(image) # calling a image compression function
                )
                print('image db created created')

        else:
            # messages.error(request, 'Map Location already added by other user', extra_tags='map_point_already_exist_error')
            print('Map Location already added by other user')
            return JsonResponse({'point_exist': True},safe=False)

    print(request.user, 'usertttttttttttt')

    return render(request, 'admin/add_dogspot.html', {'lat':lat, 'lng':lng})



@login_required
def missings_all(request):
    missing=missing_case.objects.all()

    return render(request,'admin/missing_case_a.html',{'missing':missing})

@login_required
def missing_details_all(request,pk):
    
    missing=missing_case.objects.get(pk=pk)
    return render(request,'admin/missing_details_a.html',{'missing':missing})

@login_required
def missings_your(request):
    
    missing=missing_case.objects.filter(user_id=request.user.id)
    return render(request,'admin/missing_case_y.html',{'missing':missing})

@login_required
def missing_details_your(request,pk):
    
    missing=missing_case.objects.get(pk=pk)
    return render(request,'admin/missing_details_y.html',{'missing':missing})



@login_required
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
    return render(request,'admin/missings_form.html')

@login_required
def edit(request,pk):
    edit_missing=missing_case.objects.get(pk=pk)
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
    return render(request,'admin/missing_edit.html',{'edit_missing':edit_missing})
@login_required
def delete_a(request,pk):
    missing_delete=missing_case.objects.get(pk=pk)
    missing_delete.delete()
    return redirect(missings_all)

@login_required
def delete_y(request,pk):
    missing_delete=missing_case.objects.get(pk=pk)
    missing_delete.delete()
    return redirect(missings_your)

@login_required
def comment_a(request,pk):
    if request.POST:
        commenter=request.POST.get('Comments')
        comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk),user_id=User.objects.get(pk=request.user.id))
        comment_obj.save()
        
    comm=comment.objects.filter(missing_id=pk)
    return render(request,'admin/comments_a.html',{'comm':comm})

@login_required
def comment_y(request,pk):
    if request.POST:
        commenter=request.POST.get('Comments')
        comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk),user_id=User.objects.get(pk=request.user.id))
        comment_obj.save()
        
    comm=comment.objects.filter(missing_id=pk)
    return render(request,'admin/comments_y.html',{'comm':comm})

# def comment_view(request,pk):
#     if request.POST:
#         commenter=request.POST.get('Comments')
#         comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk),user_id=User.objects.get(pk=request.user.id))
#         comment_obj.save()
#     comm=comment.objects.filter(missing_id=pk)
#     return render(request,'admin/comments.html',{'comm':comm})

@login_required
def comment_delete_all(request,pk):

    com_dele=comment.objects.get(id=pk)
    com_dele.delete()
    return redirect('/admin/comment_a/' + str(com_dele.missing_id_id))

@login_required
def comment_delete_your(request,pk):

    com_dele=comment.objects.get(id=pk)
    com_dele.delete()
    return redirect('/admin/comment_y/' + str(com_dele.missing_id_id))

@login_required
def report_list(request):
    li=missing_report.objects.all()
    return render(request,'admin/report_list.html',{'li':li})

@login_required
def report_delete_l(request,pk):
    dele=missing_report.objects.get(id=pk)
    dele.delete()
    return redirect(report_list)

@login_required
def report_all(request,pk):
    mis=missing_report.objects.filter(missing_id=pk)
    return render(request,'admin/missing_rpt_a.html',{'mis':mis})

@login_required
def report_your(request,pk):
    mis=missing_report.objects.filter(missing_id=pk)
    return render(request,'admin/missing_rpt_y.html',{'mis':mis})

@login_required
def report_delete_all(request,pk):
    dele=missing_report.objects.get(id=pk)
    dele.delete()
    return redirect('/admin/report_all/' + str(dele.missing_id_id))

@login_required
def report_delete_your(request,pk):
    dele=missing_report.objects.get(id=pk)
    dele.delete()
    return redirect('/admin/report_your/' + str(dele.missing_id_id))


@login_required
def profile(request):
    pro=User.objects.get(id=request.user.id)
    return render(request,'admin/profile.html',{'pro':pro})

@login_required
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
    return render(request,'admin/profile_update.html',{'pro_edit':pro_edit})

@login_required
def adoption_form(request):
   
    if request.POST:
        dog_name=request.POST.get('dog_name')
        owner_name=request.POST.get('owner_name')
        address=request.POST.get('Address')
        breed=request.POST.get('breed')
        dog_license=request.POST.get('License')
        vaccinated=request.POST.get('vaccinated')
        age=request.POST.get('age')
        color=request.POST.get('color')
        phone_no=request.POST.get('Phone_no')
        description=request.POST.get('Description')
        image=request.FILES['Image']
        adoption_obj=adoption(address=address,phone_no=phone_no,description=description,image=image,dog_name=dog_name,owner_name=owner_name,breed=breed,dog_license=dog_license,vaccination=vaccinated,age=age,color=color,user_id=User.objects.get(id=request.user.id))
        adoption_obj.save()
        willing_list=User.objects.filter(willing_to_adopt='yes').exclude(id=request.user.id)
        print("willing_list:",willing_list)
        for row in willing_list:
          print(row.first_name,row.id)
          adoption_req=adoption_request(user_id=User.objects.get(id=row.id), adoption_id=adoption_obj.id)
          adoption_req.save()
        messages.success(request, 'adoption')
    return render(request,'admin/adoption_form.html')

@login_required
def adoption_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'admin/adoption.html',{'adoption': adoption1})
    

@login_required
def edit_adoption(request,pk):
    edit_ad=adoption.objects.get(pk=pk,user_id=request.user.id)
    if request.POST:
        # edit_missing=missing_case.objects.get(pk=pk)
        dog_name=request.POST.get('dog_name')
        owner_name=request.POST.get('owner_name')
        address=request.POST.get('Address')
        phone_no=request.POST.get('Phone_no')
        dog_license=request.POST.get('License')
        vaccinated=request.POST.get('vaccinated')
        age=request.POST.get('age')
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
        edit_ad.dog_license=dog_license
        edit_ad.vaccination=vaccinated
        edit_ad.age=age
        edit_ad.breed=breed
        edit_ad.color=color
        edit_ad.description=description
        edit_ad.image=image
        # edit_missing.status=status
        edit_ad.save()
        messages.success(request, 'adoption')
    return render(request,'admin/adoption_edit.html',{'edit_ad':edit_ad})


@login_required
def adoption_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'admin/adoption_details.html',{'adoption2':adoption2})

@login_required
def adoption_delete(request,pk):
    ad_delete=adoption.objects.get(pk=pk)
    ad_delete.delete()
    return redirect(adoption_view)

@login_required
def adoption_all_view(request):
    
    adoption1=adoption.objects.all()
    return render(request,'admin/adoption_all.html',{'adoption': adoption1})

@login_required
def adoption_all_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'admin/adoption_all_details.html',{'adoption2':adoption2})

@login_required
def adoption_all_delete(request,pk):
    ad_delete=adoption.objects.get(pk=pk)
    ad_delete.delete()
    return redirect(adoption_all_view)

@login_required
def adoption_snd_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'admin/adoption_req_snd.html',{'adoption': adoption1})

@login_required
def request_list(request,pk):
    adoption1=adoption.objects.get(id=pk)
    ruq=adoption_request.objects.filter(adoption_id=pk)
    return render(request, 'admin/request_list.html',{'ruq':ruq,'adoption1':adoption1})

@login_required
def request_profile(request,pk):
    pro=User.objects.get(id=pk)
    return render(request,'admin/request_profile.html',{'pro':pro})

@login_required
def request_cancel(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='cancel'
    ruq.save()
    return redirect('/admin/adp_request_list/' + str(ruq.adoption_id))

@login_required
def request_send(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='active'
    ruq.save()
    return redirect('/admin/adp_request_list/' + str(ruq.adoption_id))



    


