from django.contrib import admin


from .models import Area, City, Place, Review,LikePlace
admin.site.register(Place)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Review)
admin.site.register(LikePlace)


# Register your models here.
