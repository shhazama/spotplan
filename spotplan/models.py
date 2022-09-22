from django.db import models

REQUIRED_TIME = (('1時間', '1時間'), ('2～3時間','2～3時間'), ('半日','半日'),('日中','日中'))
#AREA=(('北海道地方','北海道地方'),('東北地方','東北地方'),('関東地方','関東地方'),('中部地方','中部地方'),('近畿地方','近畿地方'),('中国地方','中国地方'),('四国地方','四国地方'),('九州地方','九州地方'))

class Place(models.Model):
    
    place_area_adress=models.URLField(max_length=100,default='-')
    place_name=models.CharField(max_length=100)
    headline=models.CharField(max_length=100)
    place_detail = models.TextField()
    place_adress=models.CharField(max_length=200)
    place_parking=models.CharField(max_length=100, null=True,blank=True)
    place_access=models.CharField(max_length=100,null=True,blank=True )
    place_opening=models.CharField(max_length=100, null=True,blank=True)
    thumbnail =models.URLField(null=True,blank=True)    
    place_url=models.URLField(null=True,blank=True)

    required_time=models.CharField(max_length=100, 
        choices= REQUIRED_TIME,null=True,blank=True )
    
    
    
    
    
   
    
   