from django.db import models

from accounts.models import User

from PIL import Image # for image compression

# # Create your models here.

class Map_Details(models.Model):
  
    ZONE_COLORS = [
        ('red', 'Red'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
    ]
    
    RADIUS_COLORS = [
        ('#FF0000', 'Red'),
        ('#FFD326', 'Yellow'),
        ('#2AAD27', 'Green'),
    ]

    KM_DISTANCE = [
        ('250', '500 Meters'),
        ('500', '1 Km'),
        ('1000', '2 Km'),
        ('1500', '3 Km'),
        ('2000', '4 Km'),
        ('2500', '5 Km'),
    ]

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    email=models.CharField(max_length=255, null=True)
    longitude=models.CharField(max_length=255 ,null=True, blank=True)
    latitude=models.CharField(max_length=255 ,null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    place_name = models.CharField(max_length=100,null=True, blank=True)
    description = models.CharField(max_length=255,null=True, blank=True)
    no_of_dogs = models.IntegerField(null=True, blank=True)
    behaviour = models.CharField(max_length=255,null=True, blank=True)
    zone = models.CharField(max_length=50,choices=ZONE_COLORS)
    radius_color = models.CharField(max_length=50, choices=RADIUS_COLORS)
    radius_color_hexcode = models.CharField(max_length=50, choices=RADIUS_COLORS)
    km_distance = models.IntegerField(choices=KM_DISTANCE)
    
    def __str__(self):
        return str(self.user)


class Dog_Pics(models.Model):
    map_id = models.ForeignKey(Map_Details, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'images')


class missing_case(models.Model):
    dog_name=models.CharField(max_length=250,blank=True,null=True)
    owner_name=models.CharField(max_length=250,blank=True,null=True)
    place=models.CharField(max_length=250,blank=True,null=True)
    phone_no=models.IntegerField()
    breed=models.CharField(max_length=250,blank=True,null=True)
    color=models.CharField(max_length=250,blank=True,null=True)
    description=models.CharField(max_length=250)
    image=models.ImageField(null=True,upload_to='image/', blank=True)
    status=models.CharField(max_length=50,default='active',null=True)
    created_at=models.DateTimeField( auto_now=True, auto_now_add=False)
    latitude=models.CharField(max_length=255,blank=True,null=True)
    longitude=models.CharField(max_length=255,blank=True,null=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=50,null=True,blank=True)


class comment(models.Model):
    comments=models.CharField(max_length=250)
    missing_id=models.ForeignKey(missing_case, on_delete=models.CASCADE)
    date=models.DateField( auto_now=True, auto_now_add=False)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class missing_report(models.Model):
    category=models.CharField(max_length=250)
    report_summery=models.CharField(max_length=250)
    missing_id=models.ForeignKey(missing_case, on_delete=models.CASCADE)
    date=models.DateField( auto_now=True, auto_now_add=False)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)




class adoption(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    dog_name=models.CharField( max_length=50)
    owner_name=models.CharField( max_length=50)
    phone_no=models.CharField(max_length=50)
    image=models.ImageField(upload_to='adoption')
    description=models.CharField(max_length=1024)
    created_at=models.DateField(auto_now=True, auto_now_add=False)
    status=models.CharField(max_length=50,default='active')
    address=models.CharField(max_length=250)
    latitude=models.CharField(max_length=250,null=True,blank=True)
    longitude=models.CharField(max_length=250,null=True,blank=True)
    breed=models.CharField(max_length=50)
    color=models.CharField(max_length=50)
    dog_license=models.CharField(max_length=50,default='no')
    vaccination=models.CharField(max_length=50,default='no')
    age=models.CharField(max_length=50,null=True,blank=True)



class adoption_request(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    adoption=models.ForeignKey(adoption, on_delete=models.CASCADE,null=True,blank=True)
    approval_request=models.CharField(max_length=50,default='active')






