from django.shortcuts import render,redirect

import folium
from folium import plugins
from django.contrib import messages

import geocoder
from user.models import missing_case
from user.models import comment
from user.models import missing_report
from accounts.models import User
from user.models import adoption,adoption_request


# Create your views here.

def dashboard(request):
    return render(request, 'admin/dashboard.html')


def users(request):
    user=User.objects.all()
    return render(request, 'admin/users.html',{'user':user})

def user_details(request,pk):
    user=User.objects.get(pk=pk)
    return render(request,'admin/user_details.html',{'user':user})


def map(request):
    state = geocoder.osm('Kumaranalloor, Kottayam, Kottayam, Kerala, India')
    map1  = folium.Map(location=[state.lat, state.lng], zoom_start=13)

    plugins.Fullscreen(position='topright').add_to(map1)

    # data = [[19, 12, 3000], [20,10,4999]]
    # data = [[19, state.lat, 3000], [20, state.lng, 4999]]
    # plugins.HeatMap(data).add_to(map1)

    data = [[9.6174363, 76.5327349], [9.618650, 76.509079], [9.670300, 76.556763], [9.718096, 76.544586], [9.63375, 76.52090]]

    for x in data:
        print(x)


        folium.Marker(
            x, 
            popup="<h1 style='text-align:center;'>Kumaranallor<br><img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGtuJgv57yb7bUXsCri1_tKp_Q372TXmWlFTShxcz_&s' /><br><a href='https://www.w3schools.com' target='_blank'>Visit</a></h1>",
            tooltip='Kumaranalloor',
            icon=folium.Icon(color="green")

        ).add_to(map1)
    
    # folium.Marker(
    #     [9.618650, 76.509079], 
    #     popup="<h1 style='text-align:center;'>Kumaranallor<br><img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGtuJgv57yb7bUXsCri1_tKp_Q372TXmWlFTShxcz_&s' /><br><a href='https://www.w3schools.com'>Visit</a></h1>",
    #     tooltip='Kumaranalloor',
    #     icon=folium.Icon(color="red", icon="info-sign"),

    # ).add_to(map1)


    map1.add_child(folium.ClickForMarker(popup=f"<a href='https://www.w3schools.com' target='_blank'>Add Dogspot</a>"))
    # map1.add_child(folium.ClickForMarker(popup=None))

    # map1.get_root().html.add_child(folium.Element('''
    # <div>
    #     <h1>Hello world</h1>
    # </div>
    # '''))

    print(map1.location, 'aaaaaaaaaaaaaaaa')

    map1 = map1._repr_html_()
    print(state.lat)
    print(state.lng)


    return render(request, 'admin/map.html', {'map': map1})



def missings_all(request):
    missing=missing_case.objects.all()

    return render(request,'admin/missing_case_a.html',{'missing':missing})

def missing_details_all(request,pk):
    
    missing=missing_case.objects.get(pk=pk)
    return render(request,'admin/missing_details_a.html',{'missing':missing})

def missings_your(request):
    
    missing=missing_case.objects.filter(user_id=request.user.id)
    return render(request,'admin/missing_case_y.html',{'missing':missing})

def missing_details_your(request,pk):
    
    missing=missing_case.objects.get(pk=pk)
    return render(request,'admin/missing_details_y.html',{'missing':missing})



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

def delete_a(request,pk):
    missing_delete=missing_case.objects.get(pk=pk)
    missing_delete.delete()
    return redirect(missings_all)


def delete_y(request,pk):
    missing_delete=missing_case.objects.get(pk=pk)
    missing_delete.delete()
    return redirect(missings_your)

def comment_a(request,pk):
    if request.POST:
        commenter=request.POST.get('Comments')
        comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk))
        comment_obj.save()
        
    comm=comment.objects.filter(missing_id=pk)
    return render(request,'admin/comments_a.html',{'comm':comm})

def comment_y(request,pk):
    if request.POST:
        commenter=request.POST.get('Comments')
        comment_obj=comment(comments=commenter,missing_id=missing_case.objects.get(pk=pk))
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

def comment_delete_all(request,pk):

    com_dele=comment.objects.get(id=pk)
    com_dele.delete()
    return redirect('/admin/comment_a/' + str(com_dele.missing_id_id))

def comment_delete_your(request,pk):

    com_dele=comment.objects.get(id=pk)
    com_dele.delete()
    return redirect('/admin/comment_y/' + str(com_dele.missing_id_id))

def report_list(request):
    li=missing_report.objects.all()
    return render(request,'admin/report_list.html',{'li':li})

def report_delete_l(request,pk):
    dele=missing_report.objects.get(id=pk)
    dele.delete()
    return redirect(report_list)

def report_all(request,pk):
    mis=missing_report.objects.filter(missing_id=pk)
    return render(request,'admin/missing_rpt_a.html',{'mis':mis})

def report_your(request,pk):
    mis=missing_report.objects.filter(missing_id=pk)
    return render(request,'admin/missing_rpt_y.html',{'mis':mis})

def report_delete_all(request,pk):
    dele=missing_report.objects.get(id=pk)
    dele.delete()
    return redirect('/admin/report_all/' + str(dele.missing_id_id))

def report_delete_your(request,pk):
    dele=missing_report.objects.get(id=pk)
    dele.delete()
    return redirect('/admin/report_your/' + str(dele.missing_id_id))



def profile(request):
    pro=User.objects.get(id=request.user.id)
    return render(request,'admin/profile.html',{'pro':pro})


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
    return render(request,'admin/adoption_form.html')


def adoption_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'admin/adoption.html',{'adoption': adoption1})
    


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
    return render(request,'admin/adoption_edit.html',{'edit_ad':edit_ad})



def adoption_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'admin/adoption_details.html',{'adoption2':adoption2})


def adoption_delete(request,pk):
    ad_delete=adoption.objects.get(pk=pk)
    ad_delete.delete()
    return redirect(adoption_view)

def adoption_all_view(request):
    
    adoption1=adoption.objects.all()
    return render(request,'admin/adoption_all.html',{'adoption': adoption1})


def adoption_all_details(request,pk):
    
    adoption2=adoption.objects.get(pk=pk)
    return render(request,'admin/adoption_all_details.html',{'adoption2':adoption2})


def adoption_all_delete(request,pk):
    ad_delete=adoption.objects.get(pk=pk)
    ad_delete.delete()
    return redirect(adoption_all_view)

def adoption_snd_view(request):
    
    adoption1=adoption.objects.filter(user_id=request.user.id)
    return render(request,'admin/adoption_req_snd.html',{'adoption': adoption1})


def request_list(request,pk):
    adoption1=adoption.objects.get(id=pk)
    ruq=adoption_request.objects.filter(adoption_id=pk)
    return render(request, 'admin/request_list.html',{'ruq':ruq,'adoption1':adoption1})


def request_profile(request,pk):
    pro=User.objects.get(id=pk)
    return render(request,'admin/request_profile.html',{'pro':pro})


def request_cancel(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='cancel'
    ruq.save()
    return redirect('/admin/adp_request_list/' + str(ruq.adoption_id))


def request_send(request,pk):
    ruq=adoption_request.objects.get(id=pk)
    ruq.approval_request='active'
    ruq.save()
    return redirect('/admin/adp_request_list/' + str(ruq.adoption_id))



    


