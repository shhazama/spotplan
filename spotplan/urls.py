
from django.urls import path
from . import views

#app_name = 'YourAppName'
urlpatterns = [
    # :
    # :
    path('upload/', views.upload, name='upload'),
    path('', views.list_view,name='list-palce'),
    #path('', views.ListPlaceView.as_view(),name='list-place'),
    path('place/<int:pk>/detail/',views.DetailPlaceView.as_view(),name='detail-place'),
    # :
]