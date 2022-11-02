# from logging.config import _LoggerConfiguration
from multiprocessing import context
from re import A
from typing_extensions import OrderedDict
from unittest import result
from django.shortcuts import render,redirect, get_object_or_404
from .models import Area, City, Place,Review, UserBank,LikePlace
import csv
import io
from django.views import generic
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE
from django.db.models import Q, Avg
import googlemaps
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse



def upload(request):
    if 'csv' in request.FILES:

        data = io.TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(data)
        for line in csv_file:
            place = Place()

            place.place_area_adress = line[0]
            place.place_name = line[1]
            place.headline = line[2]
            place.place_detail = line[3]
            place.place_adress = line[4]
            place.place_parking = line[5]
            place.place_access = line[6]
            place.place_opening = line[7]
            place.thumbnail = line[8]
            place.place_url = line[9]

            place.save()
            print('ok')

        return render(request, 'YourApp/upload.html')

    else:
        return render(request, 'YourApp/upload.html')


# class ListPlaceView(ListView):
  #  template_name = 'list_place.html'
   # model = Place
   # pagenate_by = ITEM_PER_PAGE


def list_view(request, area):
    object_list = Place.objects.filter(areas__area=area).order_by('id')

    paginator = Paginator(object_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(request,
                  'list_place.html',
                  {'object_list': object_list, 'page_obj': page_obj},)


def citylist_view(request, city):
    object_list = Place.objects.filter(city__city=city).order_by('id')
    paginator = Paginator(object_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    geo_lat_avg = page_obj.object_list.aggregate(geo_lat_avg=Avg('geo_lat'))
    geo_lng_avg = page_obj.object_list.aggregate(geo_lng_avg=Avg('geo_lng'))

    return render(request,
                  'citylist_place.html',
                  {
                      'object_list': object_list,
                      'page_obj': page_obj,
                      'map_center': {'lat': geo_lat_avg['geo_lat_avg'], 'lng': geo_lng_avg['geo_lng_avg']}
                  }
                  )

def mypage_view(request):
    object_list = LikePlace.objects.get(all)

    paginator = Paginator(object_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(request,
                  'mypage.html',
                  {'object_list': object_list, 'page_obj': page_obj},)

    

class PlaceList(generic.ListView):
    template_name = 'placelist.html'
    model =Place

class DetailPlaceView(generic.DetailView):
    template_name = 'detail_place.html'
    model = Place
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likeplace_count = self.object.likeplace_set.count()
        # ポストに対するイイね数
        context['likeplace_count'] = likeplace_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.likeplace_set.filter(user=self.request.user).exists():
            context['is_user_likplace'] = True
        else:
            context['is_user_likeplace'] = False

        return context
def likeplace(request):
    place_pk = request.POST.get('place_pk')
    context = {
        'user': f'{request.user}',
    }
    place = get_object_or_404(Place, pk=place_pk)
    like = LikePlace.objects.filter(favorite_place=place, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(favorite_place=place, user=request.user)
        context['method'] = 'create'

    context['likeplace_count'] =place.likeplace_set.count()

    return JsonResponse(context)

class HomeView(TemplateView):
    template_name = 'home.html'


def geo(request):

    def geocode(address):
        gmaps = googlemaps.Client(
            key='AIzaSyBgd0aDbXECj_riwa3iG7HnqtSSGptQpYM')
        result = gmaps.geocode(address)
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']

        return lat, lng
        # 住所リストを読み込む
        # 住所リストには　address というカラムが必須

    adresslist = Place.objects.values('place_adress', 'id')

    # 緯度経度データの取得
    # result = []  取得した緯度経度を入れておくリスト
    for ad in adresslist:
        lat, lng = geocode(ad['place_adress'])
        place = Place.objects.get(id=ad['id'])
        place.geo_lat = lat
        place.geo_lng = lng
        place.save()
        print('ok')

    return render(request, 'YourApp/upload.html')

# 8区分分別
def bunbetsu(request):
    # areag事の分別
    active_place_area = Place.objects \
        .filter(place_adress__contains='北海道')
    print(active_place_area.count())
    hokkaido = Area.objects.get(area='hokkaido')
    active_place_area.update(areas=hokkaido)
    print('北海道　ok')

    # 九州
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='沖縄県') | Q(place_adress__contains='福岡県') | Q(place_adress__contains='鹿児島県') | Q(place_adress__contains='佐賀県') | Q(place_adress__contains='長崎県') | Q(place_adress__contains='熊本県') | Q(place_adress__contains='大分県') | Q(place_adress__contains='宮崎県'))
    print(active_place_area.count())
    kyusyu = Area.objects.get(area='kyusyu')
    active_place_area.update(areas=kyusyu)
    print('九州　ok')

    # 中国
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='広島県') | Q(place_adress__contains='山口県') | Q(place_adress__contains='鳥取県') | Q(place_adress__contains='岡山県') | Q(place_adress__contains='島根県'))
    print(active_place_area.count())
    tyugoku = Area.objects.get(area='tyugoku')
    active_place_area.update(areas=tyugoku)
    print('中国　ok')

    # 四国
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='香川県') | Q(place_adress__contains='愛媛県') | Q(place_adress__contains='高知県') | Q(place_adress__contains='徳島県'))
    print(active_place_area.count())
    shikoku = Area.objects.get(area='shikoku')
    active_place_area.update(areas=shikoku)
    print('四国　ok')

    # 近畿
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='大阪府') | Q(place_adress__contains='京都府') | Q(place_adress__contains='兵庫県') | Q(place_adress__contains='奈良県') | Q(place_adress__contains='和歌山県') | Q(place_adress__contains='三重県') | Q(place_adress__contains='滋賀県'))
    print(active_place_area.count())
    kinki = Area.objects.get(area='kinki')
    active_place_area.update(areas=kinki)
    print('近畿　ok')

    # 中部
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='新潟県') | Q(place_adress__contains='富山県') | Q(place_adress__contains='石川県') | Q(place_adress__contains='福井県') | Q(place_adress__contains='山梨県') | Q(place_adress__contains='長野県') | Q(place_adress__contains='岐阜県') | Q(place_adress__contains='静岡県') | Q(place_adress__contains='愛知県'))
    print(active_place_area.count())
    tyubu = Area.objects.get(area='tyubu')
    active_place_area.update(areas=tyubu)
    print('中部　ok')

    # 関東
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='東京都') | Q(place_adress__contains='群馬県') | Q(place_adress__contains='埼玉県') | Q(place_adress__contains='千葉県') | Q(place_adress__contains='茨城県') | Q(place_adress__contains='栃木県') | Q(place_adress__contains='神奈川県'))
    print(active_place_area.count())
    kannto = Area.objects.get(area='kannto')
    active_place_area.update(areas=kannto)
    print('関東　ok')

    # 東北
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='青森県') | Q(place_adress__contains='岩手県') | Q(place_adress__contains='秋田県') | Q(place_adress__contains='宮城県') | Q(place_adress__contains='山形県') | Q(place_adress__contains='福島県'))
    print(active_place_area.count())
    touhoku = Area.objects.get(area='touhoku')
    active_place_area.update(areas=touhoku)
    print('東北　ok')

    return render(request, 'YourApp/upload.html')

# 都道府県ごとに分類


def city_touroku(request):
    # areag事の分別
    active_place_city = Place.objects \
        .filter(place_adress__contains='北海道')
    print(active_place_city.count())
    a = City.objects.get(city='j1')
    active_place_city.update(city=a)
    print('j1 ok')

    # j2登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='青森県')
    print(active_place_city.count())
    b = City.objects.get(city='j2')
    active_place_city.update(city=b)
    print('j2 ok')

    # j3登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='岩手県')
    print(active_place_city.count())
    b = City.objects.get(city='j3')
    active_place_city.update(city=b)
    print('j3 ok')

    # j4登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='宮城県')
    print(active_place_city.count())
    b = City.objects.get(city='j4')
    active_place_city.update(city=b)
    print('j4 ok')

    # j5登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='秋田県')
    print(active_place_city.count())
    b = City.objects.get(city='j5')
    active_place_city.update(city=b)
    print('j5 ok')

    # j6登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='山形県')
    print(active_place_city.count())
    b = City.objects.get(city='j6')
    active_place_city.update(city=b)
    print('j6 ok')

    # j7登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='福島県')
    print(active_place_city.count())
    b = City.objects.get(city='j7')
    active_place_city.update(city=b)
    print('j7 ok')

    # j8登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='茨城県')
    print(active_place_city.count())
    b = City.objects.get(city='j8')
    active_place_city.update(city=b)
    print('j8 ok')

    # j9登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='栃木県')
    print(active_place_city.count())
    b = City.objects.get(city='j9')
    active_place_city.update(city=b)
    print('j9 ok')

    # j10登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='群馬県')
    print(active_place_city.count())
    b = City.objects.get(city='j10')
    active_place_city.update(city=b)
    print('j10 ok')

    # j11登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='埼玉県')
    print(active_place_city.count())
    b = City.objects.get(city='j11')
    active_place_city.update(city=b)
    print('j11 ok')

    # j12登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='千葉県')
    print(active_place_city.count())
    b = City.objects.get(city='j12')
    active_place_city.update(city=b)
    print('j12 ok')

    # j13登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='東京都')
    print(active_place_city.count())
    b = City.objects.get(city='j13')
    active_place_city.update(city=b)
    print('j13 ok')

    # j14登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='神奈川県')
    print(active_place_city.count())
    b = City.objects.get(city='j14')
    active_place_city.update(city=b)
    print('j14 ok')

    # j15登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='新潟県')
    print(active_place_city.count())
    b = City.objects.get(city='j15')
    active_place_city.update(city=b)
    print('j15 ok')

    # j16登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='富山県')
    print(active_place_city.count())
    b = City.objects.get(city='j16')
    active_place_city.update(city=b)
    print('j16 ok')

    # j17登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='石川県')
    print(active_place_city.count())
    b = City.objects.get(city='j17')
    active_place_city.update(city=b)
    print('j17 ok')

    # j18登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='福井県')
    print(active_place_city.count())
    b = City.objects.get(city='j18')
    active_place_city.update(city=b)
    print('j18 ok')

    # j19登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='山梨県')
    print(active_place_city.count())
    b = City.objects.get(city='j19')
    active_place_city.update(city=b)
    print('j19 ok')

    # j20登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='長野県')
    print(active_place_city.count())
    b = City.objects.get(city='j20')
    active_place_city.update(city=b)
    print('j20 ok')

    # j21登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='岐阜県')
    print(active_place_city.count())
    b = City.objects.get(city='j21')
    active_place_city.update(city=b)
    print('j21 ok')

    # j22登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='静岡県')
    print(active_place_city.count())
    b = City.objects.get(city='j22')
    active_place_city.update(city=b)
    print('j22 ok')

    # j23登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='愛知県')
    print(active_place_city.count())
    b = City.objects.get(city='j23')
    active_place_city.update(city=b)
    print('j23 ok')

    # j24登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='三重県')
    print(active_place_city.count())
    b = City.objects.get(city='j24')
    active_place_city.update(city=b)
    print('j24 ok')

    # j25登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='滋賀県')
    print(active_place_city.count())
    b = City.objects.get(city='j25')
    active_place_city.update(city=b)
    print('j25 ok')

    # j26登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='京都府')
    print(active_place_city.count())
    b = City.objects.get(city='j26')
    active_place_city.update(city=b)
    print('j26 ok')

    # j27登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='大阪府')
    print(active_place_city.count())
    b = City.objects.get(city='j27')
    active_place_city.update(city=b)
    print('j27 ok')

    # j28登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='兵庫県')
    print(active_place_city.count())
    b = City.objects.get(city='j28')
    active_place_city.update(city=b)
    print('j28 ok')

    # j29登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='奈良県')
    print(active_place_city.count())
    b = City.objects.get(city='j29')
    active_place_city.update(city=b)
    print('j29 ok')

    # j30登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='和歌山県')
    print(active_place_city.count())
    b = City.objects.get(city='j30')
    active_place_city.update(city=b)
    print('j30 ok')

    # j31登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='鳥取県')
    print(active_place_city.count())
    b = City.objects.get(city='j31')
    active_place_city.update(city=b)
    print('j31 ok')

    # j32登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='島根県')
    print(active_place_city.count())
    b = City.objects.get(city='j32')
    active_place_city.update(city=b)
    print('j32 ok')

    # j33登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='岡山県')
    print(active_place_city.count())
    b = City.objects.get(city='j33')
    active_place_city.update(city=b)
    print('j33 ok')

    # j34登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='広島県')
    print(active_place_city.count())
    b = City.objects.get(city='j34')
    active_place_city.update(city=b)
    print('j34 ok')

    # j35登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='山口県')
    print(active_place_city.count())
    b = City.objects.get(city='j35')
    active_place_city.update(city=b)
    print('j35 ok')

    # j36登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='徳島県')
    print(active_place_city.count())
    b = City.objects.get(city='j36')
    active_place_city.update(city=b)
    print('j36 ok')

    # j37登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='香川県')
    print(active_place_city.count())
    b = City.objects.get(city='j37')
    active_place_city.update(city=b)
    print('j37 ok')

    # j38登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='愛媛県')
    print(active_place_city.count())
    b = City.objects.get(city='j38')
    active_place_city.update(city=b)
    print('j38 ok')

    # j39登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='高知県')
    print(active_place_city.count())
    b = City.objects.get(city='j39')
    active_place_city.update(city=b)
    print('j39 ok')

    # j40登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='福岡県')
    print(active_place_city.count())
    b = City.objects.get(city='j40')
    active_place_city.update(city=b)
    print('j40 ok')

    # j41登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='佐賀県')
    print(active_place_city.count())
    b = City.objects.get(city='j41')
    active_place_city.update(city=b)
    print('j41 ok')

    # j42登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='長崎県')
    print(active_place_city.count())
    b = City.objects.get(city='j42')
    active_place_city.update(city=b)
    print('j42 ok')

    # j43登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='熊本県')
    print(active_place_city.count())
    b = City.objects.get(city='j43')
    active_place_city.update(city=b)
    print('j43 ok')

    # j44登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='大分県')
    print(active_place_city.count())
    b = City.objects.get(city='j44')
    active_place_city.update(city=b)
    print('j44 ok')

    # j45登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='宮崎県')
    print(active_place_city.count())
    b = City.objects.get(city='j45')
    active_place_city.update(city=b)
    print('j45 ok')

    # j46登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='鹿児島県')
    print(active_place_city.count())
    b = City.objects.get(city='j46')
    active_place_city.update(city=b)
    print('j46 ok')

    # j47登録
    active_place_city = Place.objects \
        .filter(place_adress__contains='沖縄県')
    print(active_place_city.count())
    b = City.objects.get(city='j47')
    active_place_city.update(city=b)
    print('j47 ok')

    return render(request, 'YourApp/upload.html')

#@login_required
#ファンクションベースわからない
#def followplace(request,place_name):
    
 #    object_place = UserBank.objects
  #   place = get_object_or_404(Place, pk=place_name)
   #  
    # object_place.add(place)
    
     #return redirect(request,'detail-name')

class CreateReviewView(LoginRequiredMixin,CreateView):
    model = Review
    fields=('place','title','text','rate')
    template_name = 'review_form.html'
    #他のモデルからデータの取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place']=Place.objects.get(pk=self.kwargs['place_id'])
        print(context)
        return context
    #フォームに送信し問題ないか確認市問題なければ保存
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    def get_success_url(self):
       
        return reverse('detail-place', kwargs={'pk':self.object.place.id})
class FollowView(LoginRequiredMixin,CreateView):
    model = UserBank
    fields=('user','favorite_place')
    template_name = 'follow.html'
    #他のモデルからデータの取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place']=Place.objects.get(pk=self.kwargs['place_id'])
        place=[]
        place.article_set.add(context)
        print(context)
        return context
    def form_valid(self, form):
        form.instance.user = self.request.user
        user= form.instance.user
        
        print(user)

        return super().form_valid(form)