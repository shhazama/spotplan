
from django.urls import path
from . import views

#app_name = 'YourAppName'
urlpatterns = [
    # :
    # :
    path('upload/', views.upload, name='upload'),
    path('bunbetsu/', views.bunbetsu, name='bunbetsu'),
    path('city_touroku/', views.city_touroku, name='city_touroku'),
    path('geo/', views.geo, name='geo'),
    path('area/<str:area>/', views.list_view,name='list-palce'),
    path('home/<str:city>/', views.citylist_view,name='citylist-palce'),
    path('place/<int:pk>/detail/',views.DetailPlaceView.as_view(),name='detail-place'),
    path('',views.HomeView.as_view(),name='home'),
    path('like_for_place/', views.likeplace, name='likeplace'),  
    path('mypage/',views.mypage_view,name='mypage'),
    path('detail/<int:place_id>/review/', views.CreateReviewView.as_view(),name='review'),
    path('placelist/', views.PlaceList.as_view(), name='placelist'),
    
    # :
]