from django.db import models
from django.contrib.auth.models import User
from.consts import MAX_RATE


RATE_CHOICES =[(x,str(x)) for x in range(0, MAX_RATE + 1)]
REQUIRED_TIME = (('1時間', '1時間'), ('2～3時間','2～3時間'), ('半日','半日'),('日中','日中'))
AREA=(('hokkaido','北海道地方'),('touhoku','東北地方'),('kannto','関東地方'),('tyubu','中部地方'),('kinki','近畿地方'),('tyugoku','中国地方'),('shikoku','四国地方'),('kyusyu','九州地方'))
KEN=(('j1','北海道'),('j2','青森県'),('j3','岩手県'),('j4','宮城県'),('j5','秋田県'),('j6','山形県'),('j7','福島県'),('j8','茨城県'),('j9','栃木県'),('j10','群馬県'),('j11','埼玉県'),('j12','千葉県'),('j13','東京都'),('j14','神奈川県'),('j15','新潟県'),('j16','富山県'),('j17','石川県'),('j18','福井県'),('j19','山梨県'),('j20','長野県'),('j21','岐阜県'),('j22','静岡県'),('j23','愛知県'),('j24','三重県'),('j25','滋賀県'),('j26','京都府'),('j27','大阪府'),('j28','兵庫県'),('j29','奈良県'),('j30','和歌山県'),('j31','鳥取県'),('j32','島根県'),('j33','岡山県'),('j34','広島県'),('j35','山口県'),('j36','徳島県'),('j37','香川県'),('j38','愛媛県'),('j39','高知県'),('j40','福岡県'),('j41','佐賀県'),('j42','長崎県'),('j43','熊本県'),('j44','大分県'),('j45','宮崎県'),('j46','鹿児島県'),('j47','沖縄県'))
class Area(models.Model):
    def __str__(self) -> str:
        #choices リスト右側　get_***_deisplay()
        return self.get_area_display()
    area=models.CharField(
        max_length=100,
        choices = AREA
    )

class City(models.Model):
    def __str__(self) -> str:
        #choices リスト右側　get_***_deisplay()
        return self.get_city_display()
    city=models.CharField(
        max_length=100,
        choices = KEN
    )

class Place(models.Model):
    def __str__(self) -> str:
        #choices リスト右側　get_***_deisplay()
        return self.place_name
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
    areas=models.ForeignKey(Area, on_delete=models.CASCADE,default=None,null=True,blank=True)
    required_time=models.CharField(max_length=100, 
        choices= REQUIRED_TIME,null=True,blank=True )
    city=models.ForeignKey(City, on_delete=models.CASCADE,default=None,null=True,blank=True)
    geo_lat=models.FloatField(null=True,blank=True )
    geo_lng=models.FloatField(null=True,blank=True )

class UserBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_place=models.ManyToManyField(Place)  

#未使用（フォロー関係時に使用）    
class FavUser(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='send_user')

    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receive_user')

class Review(models.Model) :
    place=models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    #number = models.IntegerField()
    text = models.TextField()
    rate=models.IntegerField(choices=RATE_CHOICES)
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE)


    def _str_ (self) :
        return self.title
    
    
   
    
    
   
    
   