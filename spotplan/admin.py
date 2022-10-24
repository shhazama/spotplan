from django.contrib import admin
from .models import Area, City, Place, Review, UserBank
admin.site.register(Place)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(UserBank)
admin.site.register(Review)


# Register your models here.
