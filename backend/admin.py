from django.contrib import admin

# Register your models here.
from .models import User, Car, Appointment, Manufacturer, Codes, Mechanic

admin.site.register(User)
admin.site.register(Car)
admin.site.register(Appointment)
admin.site.register(Manufacturer)
admin.site.register(Mechanic)
