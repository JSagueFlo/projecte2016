from django.contrib import admin
from .models import Centre, Boia

# Register your models here.


class CentreAdmin(admin.ModelAdmin):
    list_display = ('name', 'nie')
    

class BoiaAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'centre')

admin.site.register(Centre, CentreAdmin)
admin.site.register(Boia, BoiaAdmin)