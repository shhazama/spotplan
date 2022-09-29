from re import A
from django.shortcuts import render
from .models import Area, Place
import csv
import io
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE


def upload(request):
    if 'csv' in request.FILES:
        
        data = io.TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(data)
        for line in csv_file:
            place=Place() 
           
            place.place_area_adress= line[0]
            place.place_name = line[1]
            place.headline = line[2]
            place.place_detail = line[3]
            place.place_adress =line[4]
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


#class ListPlaceView(ListView):
  #  template_name = 'list_place.html'
   # model = Place
   # pagenate_by = ITEM_PER_PAGE


def list_view(request):
    object_list = Place.objects.order_by('-id')
   
    paginator =Paginator(object_list, ITEM_PER_PAGE)
    page_number=request.GET.get('page',1)
    page_obj=paginator.page(page_number)

    

    return render(request, 
          'list_place.html',
          {'object_list': object_list, 'page_obj':page_obj },)

  
class DetailPlaceView(DetailView):
    template_name = 'detail_place.html'
    model = Place
    
#area_ view未完成
def area_view(request):
    object_list = Place.objects.order_by('-id')
    obj_area= Area.objects.order_by('-id')
    paginator =Paginator(object_list, ITEM_PER_PAGE)
    page_number=request.GET.get('page',1)
    page_obj=paginator.page(page_number)

   #active_place_area = Place.objects \
    #.filter(place_adress__contains='北海道')\
    #.exclude(area="hokkaido")\
    #.values("area") 
    
   #print(active_place_area)
   #return render(request, 
    #      'area.html',
     #     )

