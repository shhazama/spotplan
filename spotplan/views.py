# from logging.config import _LoggerConfiguration
from multiprocessing import context
from re import A
from typing_extensions import OrderedDict
from unittest import result
from django.shortcuts import render,redirect, get_object_or_404
from .models import Area, City, Place,Review,LikePlace
import csv
import io
from django.views import generic
from django.views.generic import CreateView, TemplateView,ListView
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
  place = Place.objects.order_by('-id')
  likeplace = LikePlace.objects.filter(user=request.user).order_by('favorite_place__id')
  paginator = Paginator(likeplace, ITEM_PER_PAGE)
  page_number = request.GET.get('page', 1)
  page_obj = paginator.page(page_number)
  
  return render(request,'mypage.html',{'likeplace': likeplace, 'page_obj': page_obj,'place_obj': place})
    

class PlaceList(generic.ListView):
    template_name = 'placelist.html'
    model =Place


class DetailPlaceView(generic.DetailView):
    template_name = 'detail_place.html'
    model = Place
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likeplace_count = self.object.likeplace_set.count()
        # ?????????????????????????????????
        context['likeplace_count'] = likeplace_count
        # ??????????????????????????????????????????????????????????????????
        if self.request.user.is_authenticated and self.object.likeplace_set.filter(user=self.request.user).exists():
            context['is_user_likeplace'] = True
        else:
            context['is_user_likeplace'] = False

        return context
@login_required
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
        # ??????????????????????????????
        # ????????????????????????address ???????????????????????????

    adresslist = Place.objects.values('place_adress', 'id')

    # ??????????????????????????????
    # result = []  ???????????????????????????????????????????????????
    for ad in adresslist:
        lat, lng = geocode(ad['place_adress'])
        place = Place.objects.get(id=ad['id'])
        place.geo_lat = lat
        place.geo_lng = lng
        place.save()
        print('ok')

    return render(request, 'YourApp/upload.html')

# 8????????????
def bunbetsu(request):
    # areag????????????
    active_place_area = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_area.count())
    hokkaido = Area.objects.get(area='hokkaido')
    active_place_area.update(areas=hokkaido)
    print('????????????ok')

    # ??????
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='????????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????'))
    print(active_place_area.count())
    kyusyu = Area.objects.get(area='kyusyu')
    active_place_area.update(areas=kyusyu)
    print('?????????ok')

    # ??????
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????'))
    print(active_place_area.count())
    tyugoku = Area.objects.get(area='tyugoku')
    active_place_area.update(areas=tyugoku)
    print('?????????ok')

    # ??????
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????'))
    print(active_place_area.count())
    shikoku = Area.objects.get(area='shikoku')
    active_place_area.update(areas=shikoku)
    print('?????????ok')

    # ??????
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='????????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????'))
    print(active_place_area.count())
    kinki = Area.objects.get(area='kinki')
    active_place_area.update(areas=kinki)
    print('?????????ok')

    # ??????
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????'))
    print(active_place_area.count())
    tyubu = Area.objects.get(area='tyubu')
    active_place_area.update(areas=tyubu)
    print('?????????ok')

    # ??????
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='????????????'))
    print(active_place_area.count())
    kannto = Area.objects.get(area='kannto')
    active_place_area.update(areas=kannto)
    print('?????????ok')

    # ??????
    active_place_area = Place.objects \
        .filter(Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????') | Q(place_adress__contains='?????????'))
    print(active_place_area.count())
    touhoku = Area.objects.get(area='touhoku')
    active_place_area.update(areas=touhoku)
    print('?????????ok')

    return render(request, 'YourApp/upload.html')

# ???????????????????????????


def city_touroku(request):
    # areag????????????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    a = City.objects.get(city='j1')
    active_place_city.update(city=a)
    print('j1 ok')

    # j2??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j2')
    active_place_city.update(city=b)
    print('j2 ok')

    # j3??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j3')
    active_place_city.update(city=b)
    print('j3 ok')

    # j4??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j4')
    active_place_city.update(city=b)
    print('j4 ok')

    # j5??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j5')
    active_place_city.update(city=b)
    print('j5 ok')

    # j6??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j6')
    active_place_city.update(city=b)
    print('j6 ok')

    # j7??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j7')
    active_place_city.update(city=b)
    print('j7 ok')

    # j8??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j8')
    active_place_city.update(city=b)
    print('j8 ok')

    # j9??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j9')
    active_place_city.update(city=b)
    print('j9 ok')

    # j10??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j10')
    active_place_city.update(city=b)
    print('j10 ok')

    # j11??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j11')
    active_place_city.update(city=b)
    print('j11 ok')

    # j12??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j12')
    active_place_city.update(city=b)
    print('j12 ok')

    # j13??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j13')
    active_place_city.update(city=b)
    print('j13 ok')

    # j14??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='????????????')
    print(active_place_city.count())
    b = City.objects.get(city='j14')
    active_place_city.update(city=b)
    print('j14 ok')

    # j15??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j15')
    active_place_city.update(city=b)
    print('j15 ok')

    # j16??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j16')
    active_place_city.update(city=b)
    print('j16 ok')

    # j17??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j17')
    active_place_city.update(city=b)
    print('j17 ok')

    # j18??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j18')
    active_place_city.update(city=b)
    print('j18 ok')

    # j19??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j19')
    active_place_city.update(city=b)
    print('j19 ok')

    # j20??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j20')
    active_place_city.update(city=b)
    print('j20 ok')

    # j21??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j21')
    active_place_city.update(city=b)
    print('j21 ok')

    # j22??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j22')
    active_place_city.update(city=b)
    print('j22 ok')

    # j23??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j23')
    active_place_city.update(city=b)
    print('j23 ok')

    # j24??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j24')
    active_place_city.update(city=b)
    print('j24 ok')

    # j25??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j25')
    active_place_city.update(city=b)
    print('j25 ok')

    # j26??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j26')
    active_place_city.update(city=b)
    print('j26 ok')

    # j27??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j27')
    active_place_city.update(city=b)
    print('j27 ok')

    # j28??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j28')
    active_place_city.update(city=b)
    print('j28 ok')

    # j29??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j29')
    active_place_city.update(city=b)
    print('j29 ok')

    # j30??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='????????????')
    print(active_place_city.count())
    b = City.objects.get(city='j30')
    active_place_city.update(city=b)
    print('j30 ok')

    # j31??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j31')
    active_place_city.update(city=b)
    print('j31 ok')

    # j32??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j32')
    active_place_city.update(city=b)
    print('j32 ok')

    # j33??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j33')
    active_place_city.update(city=b)
    print('j33 ok')

    # j34??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j34')
    active_place_city.update(city=b)
    print('j34 ok')

    # j35??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j35')
    active_place_city.update(city=b)
    print('j35 ok')

    # j36??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j36')
    active_place_city.update(city=b)
    print('j36 ok')

    # j37??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j37')
    active_place_city.update(city=b)
    print('j37 ok')

    # j38??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j38')
    active_place_city.update(city=b)
    print('j38 ok')

    # j39??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j39')
    active_place_city.update(city=b)
    print('j39 ok')

    # j40??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j40')
    active_place_city.update(city=b)
    print('j40 ok')

    # j41??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j41')
    active_place_city.update(city=b)
    print('j41 ok')

    # j42??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j42')
    active_place_city.update(city=b)
    print('j42 ok')

    # j43??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j43')
    active_place_city.update(city=b)
    print('j43 ok')

    # j44??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j44')
    active_place_city.update(city=b)
    print('j44 ok')

    # j45??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j45')
    active_place_city.update(city=b)
    print('j45 ok')

    # j46??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='????????????')
    print(active_place_city.count())
    b = City.objects.get(city='j46')
    active_place_city.update(city=b)
    print('j46 ok')

    # j47??????
    active_place_city = Place.objects \
        .filter(place_adress__contains='?????????')
    print(active_place_city.count())
    b = City.objects.get(city='j47')
    active_place_city.update(city=b)
    print('j47 ok')

    return render(request, 'YourApp/upload.html')

class CreateReviewView(LoginRequiredMixin,CreateView):
    model = Review
    fields=('place','title','text','rate')
    template_name = 'review_form.html'
    #???????????????????????????????????????
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place']=Place.objects.get(pk=self.kwargs['place_id'])
        print(context)
        return context
    #????????????????????????????????????????????????????????????????????????
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    def get_success_url(self):
       
        return reverse('detail-place', kwargs={'pk':self.object.place.id})


class LocationMapView(generic.ListView):
    template_name = 'location_map.html'
    model = Place


