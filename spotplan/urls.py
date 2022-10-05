
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

    path('<str:area>/', views.list_view,name='list-palce'),
    path('home/<str:city>/', views.citylist_view,name='citylist-palce'),
    path('place/<int:pk>/detail/',views.DetailPlaceView.as_view(),name='detail-place'),
    path('',views.HomeView.as_view(),name='home'),
    # :
]