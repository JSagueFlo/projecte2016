from django.contrib import admin
from .models import Centre, Boia, Registre_boia

# Register your models here.


class CentreAdmin(admin.ModelAdmin):
    list_display = ('name', 'nie')
    

class BoiaAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'centre')

class RegistreBoiaAdmin(admin.ModelAdmin):
	list_display = ('boia', 'timestamp')

admin.site.register(Centre, CentreAdmin)
admin.site.register(Boia, BoiaAdmin)
admin.site.register(Registre_boia, RegistreBoiaAdmin)