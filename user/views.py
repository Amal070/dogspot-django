from django.shortcuts import render, redirect

from user.models import Map_Details, Dog_Pics ,dogspot_report
from django.contrib import messages

from user.models import missing_case
from user.models import comment
from user.models import missing_report
from user.models import adoption,adoption_request


from django.http import JsonResponse, HttpRequest, HttpResponse


import geocoder # for getting map location(latitude, longitude)

from accounts.models import User

import os

from PIL import Image # for image compression
from io import BytesIO # for image compression

# Create your views here.

from accounts.models import User
from django.contrib.auth.decorators import login_required



# dashboard
@login_required
def dashboard(request):
    user_count = User.objects.exclude(role = 'admin').count()
    total_zones = Map_Details.objects.count()
    red_zones = Map_Details.objects.filter(zone='red').count()
    yellow_zones = Map_Details.objects.filter(zone='yellow').count()
    green_zones = Map_Details.objects.filter(zone='green').count()


    print(user_count, 'testing')
    context = {'user_count': user_count ,'total_zones':total_zones,'red_zones':red_zones,'yellow_zones':yellow_zones,'green_zones':green_zones}
    return render(request, 'user/dashboard.html', context)

# show all dogspot marker in map
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
    return render(request, 'user/map_view.html', context)

@login_required
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
    map_db = Map_Details.objects.all()
    context = {'lat':latlng.lat, 'lng':latlng.lng, 'map_db' : map_db}
    return render(request, 'user/static_dogspot_marker_map.html', context)



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

    return render(request, 'user/add_dogspot.html', {'lat':lat, 'lng':lng})
@login_required
def dogspot_list(request):
    map_data = Map_Details.objects.filter(user=request.user.id)
    # print(map_data, request.user.role)
    context = {'map_data' : map_data }
    return render(request, 'user/dogspot_list.html', context)

# update
@login_required
def dogspot_update(request):
    if request.method == 'POST' and not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        object_id = request.POST.get('id')
        print(object_id, 'object_id')

        if Map_Details.objects.filter(user=request.user.id, id=object_id).exists():
            single_map_object = Map_Details.objects.filter(user=request.user.id, id=object_id).first()
            print(single_map_object.id, single_map_object.place_name)

            context = {'single_map_object' : single_map_object}
            return render(request, 'user/dogspot_update.html', context)


    # def is_ajax(request):
    #     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    # if request.is_ajax():
    # if is_ajax(request=request):
    # if HttpRequest.is_ajax()
        
    # if isinstance(request, HttpRequest) and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    
    # ajax form area
    elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
        object_id = request.POST.get('id')
        length = request.POST.get('length')
        place_name = request.POST.get('place_name')
        description = request.POST.get('description')
        no_of_dogs = request.POST.get('no_of_dogs')
        behaviour = request.POST.get('behaviour')
        # images = request.FILES.getlist('images1')
        km = request.POST.get('km')

        print(object_id, 'object_id')
        print('place_name', place_name)
        print('description', description)
        print('no_of_dogs', no_of_dogs)
        print('behaviour', behaviour)
        print('km:', km)


        if Map_Details.objects.filter(user=request.user.id, id=object_id).exists():
            map_object = Map_Details.objects.get(user=request.user.id, id=object_id)


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

            map_object.place_name = place_name
            map_object.description = description
            map_object.no_of_dogs = no_of_dogs
            map_object.behaviour = behaviour
            map_object.zone = zone['zone']
            map_object.radius_color=zone['radius_color']
            map_object.radius_color_hexcode=zone['radius_color_hexcode']
            map_object.km_distance=km

            map_object.save() # re-saving old data with new data


            dog_pics_db = map_object.dog_pics_set.all() # all child images of "Map_Details" table (reverse relationship) 

            dog_pics_db_images_length = dog_pics_db.count() # all images count(length)

            print('count :', dog_pics_db_images_length)
            print('length :' , length)



            # only check if new image found
            # condition for checking new image comes from "form" or not
            if dog_pics_db_images_length == 1 or dog_pics_db_images_length != int(length):
                print('changes detected ...............................')

                # deleting all "old-images" from media folder
                for dog_pics_row in map_object.dog_pics_set.all():

                    if len(request.FILES) != 0:
                        if dog_pics_row.image and os.path.exists(dog_pics_row.image.path):
                            os.remove(dog_pics_row.image.path) # removing the "old-image" from media folder
                            print('old image removed')

            
                dog_pics_db.delete() # deleting all image url objects from database "image" field


                # adding new "image urls" to database and "image files" to media folder
                for file_num in range(0, int(length)):
                    image = request.FILES.get(f'images{file_num}')
                    print('image : ', image, 'form image value')

                    # adding images to database and media folder
                    Dog_Pics.objects.create(
                        map_id = map_object,
                        # image = image
                        image = image_compressor(image) # calling a image compression function
                    )
                    print('image db again created')


            else:
                print('no image change detected...............................')

            # for dog_pics_row in map_object.dog_pics_set.all():
            #     print(dog_pics_row.image.name.split('/')[-1], 'database value')        

        return JsonResponse({'status': True},safe=False)

    else:
        return redirect(dogspot_list)

@login_required
def dogspot_delete(request):
    if request.method == 'POST':
        object_id = request.POST.get('delete_id')
        if Map_Details.objects.filter(user=request.user.id, id=object_id).exists():
            map_object = Map_Details.objects.get(user=request.user.id, id=object_id)

            print('Place Name:', map_object.place_name)


            dog_pics_db = map_object.dog_pics_set.all() # all child images of "Map_Details" table (reverse relationship)

            # deleting all "old-images" from media folder
            for dog_pics_row in dog_pics_db:

                # if len(request.FILES) != 0:
                if dog_pics_row.image and os.path.exists(dog_pics_row.image.path):
                    os.remove(dog_pics_row.image.path) # removing the "old-image" from media folder
                    print('old image removed')

            messages.success(request, map_object.place_name , extra_tags='delete_msg')
        
            dog_pics_db.delete() # deleting all image url objects from database
            print('All Dog_pics db deleted sucessfully')
            map_object.delete() # deleting map object form database
            print('Map_Details db deleted sucessfully')


            return redirect('user.dogspot_list')
    
        else:
            return redirect('user.dashboard')
    
    else:
        return redirect('user.dashboard')


# def all_dogspot_list(request):
#     return render(request, 'user/all_dogspot_list.html')


# def profile(request):
#     return render(request, 'user/profile.html')

# def profile_update(request):
#     return render(request, 'user/profile_update.html')

def dogspot_rpt(request,pk):
    if request.POST:
        category=request.POST.get('category')
        summery=request.POST.get('summery')
        report_obj=dogspot_report(category=category,report_summery=summery,user_id=User.objects.get(id=request.user.id),map_id=Map_Details.objects.get(pk=pk))
        report_obj.save()
    return render(request,'user/dogspot_report.html')


@login_required
def dogspot_report_list(request):
    li=dogspot_report.objects.filter(user_id=request.user.id)
    return render(request,'user/dogspot_report_list.html',{'li':li})


@login_required
def dogspot_report_delete(request,pk):
    dele=dogspot_report.objects.filter(user_id=request.user.id,id=pk)
    dele.delete()
    return redirect(dogspot_report_list)



@login_required
def settings(request):
    return render(request, 'user/profile.html')

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
    return render(request,'user/missing_form.html')

@login_required
def missings(request):
    
    missing=missing_case.objects.filter(user_id=request.user.id)
    return render(request,'user/missing_case.html',{'missing':missing})

@login_required
def missing_details(request,pk):
    
    missing=missing_case.objects.get(pk=pk)
    return render(request,'user/missing_details.html',{'missing':missing})

@login_required
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

@login_required
def delete(request,pk):
    missing_delete=missing_case.objects.get(pk=pk)
    missing_delete.delete()
    return redirect(missings)


@login_required
def comment_view(request,pk):
    if request.POST:
        commenter=request.POST.get('Comments')
        comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk),user_id=User.objects.get(pk=request.user.id))
        comment_obj.save()
    comm=comment.objects.filter(missing_id=pk)
    return render(request,'user/comments.html',{'comm':comm})

@login_required
def comment_delete(request,pk):

    com_dele=comment.objects.get(id=pk)
    com_dele.delete()
    return redirect('/user/comment/' + str(com_dele.missing_id_id))


@login_required
def missing_rpt(request,pk):
    if request.POST:
        category=request.POST.get('category')
        summery=request.POST.get('summery')
        report_obj=missing_report(category=category,report_summery=summery,user_id=User.objects.get(id=request.user.id),missing_id=missing_case.objects.get(pk=pk))
        report_obj.save()
    return render(request,'user/missing_report.html')

@login_required
def report_case(request,pk):
    mis=missing_report.objects.filter(missing_id=pk)
    return render(request,'user/missing_rpt_list.html',{'mis':mis})

@login_required
def report_list(request):
    li=missing_report.objects.filter(user_id=request.user.id)
    return render(request,'user/report_list.html',{'li':li})



@login_required
def report_delete(request,pk):
    dele=missing_report.objects.filter(user_id=request.user.id,id=pk)
    dele.delete()
    return redirect(report_list)

@login_required
def profile(request):
    pro=User.objects.get(id=request.user.id)
    return render(request,'user/profile.html',{'pro':pro})

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
    return render(request,'user/profile_update.html',{'pro_edit':pro_edit})


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
    return render(request,'user/adoption_form.html')


@login_required
def adoption_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'user/adoption.html',{'adoption': adoption1})


@login_required
def edit_adoption(request,pk):
    edit_ad=adoption.objects.get(pk=pk,user_id=request.user.id)
    if request.POST:
        # edit_missing=missing_case.objects.get(pk=pk)
        dog_name=request.POST.get('dog_name')
        owner_name=request.POST.get('owner_name')
        address=request.POST.get('Address')
        phone_no=request.POST.get('Phone_no')
        breed=request.POST.get('breed')
        dog_license=request.POST.get('License')
        vaccinated=request.POST.get('vaccinated')
        age=request.POST.get('age')
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
        edit_ad.dog_license=dog_license
        edit_ad.vaccination=vaccinated
        edit_ad.age=age
        edit_ad.color=color
        edit_ad.description=description
        edit_ad.image=image
        # edit_missing.status=status
        edit_ad.save()
        messages.success(request, 'adoption')
    return render(request,'user/adoption_edit.html',{'edit_ad':edit_ad})


@login_required
def adoption_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'user/adoption_details.html',{'adoption2':adoption2})


@login_required
def adoption_delete(request,pk):
    ad_delete=adoption.objects.get(pk=pk)
    ad_delete.delete()
    return redirect(adoption_view)


@login_required
def adoption_snd_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'user/adoption_req_snd.html',{'adoption': adoption1})

@login_required
def adoption_snd_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'user/adoption_snd_details.html',{'adoption2':adoption2})

@login_required
def request_list(request,pk):
    adoption1=adoption.objects.get(id=pk)
    ruq=adoption_request.objects.filter(adoption_id=pk)
    return render(request, 'user/request_list.html',{'ruq':ruq,'adoption1':adoption1})

@login_required
def request_profile(request,pk):
    pro=User.objects.get(id=pk)
    return render(request,'user/request_profile.html',{'pro':pro})

@login_required
def request_cancel(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='cancel'
    ruq.save()
    return redirect('/user/adp_request_list/' + str(ruq.adoption_id))

@login_required
def request_send(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='active'
    ruq.save()
    return redirect('/user/adp_request_list/' + str(ruq.adoption_id))

@login_required
def received_list(request):
    ruq=adoption_request.objects.filter(user_id=request.user.id).exclude(approval_request='cancel')
    print("req:",ruq)
    return render(request, 'user/received_list.html',{'ruq':ruq})

@login_required
def request_accept(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='accept'
    ruq.save()
    return redirect(received_list)

@login_required
def request_reject(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='reject'
    ruq.save()
    return redirect(received_list)

@login_required
def recived_cancel(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='active'
    ruq.save()
    return redirect(received_list)


def is_willing(request):
    if request.POST:
        willing=request.POST.get('is_willing')      
        print("is_willing",willing)
        w=User.objects.get(id=request.user.id)
        if willing or willing == 'yes':
            w.willing_to_adopt='yes'
            w.save()
        else:
            w.willing_to_adopt='no'
            w.save()
            print('your already selected no!')
            
    return redirect(received_list)

    






    

     







    


        

   


