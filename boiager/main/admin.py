from django.contrib import admin
from .models import Centre, Boia, Registre_boia, Token, Slider

# Register your models here.


class CentreAdmin(admin.ModelAdmin):
    list_display = ('name', 'nie')

class BoiaAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'centre')

class RegistreBoiaAdmin(admin.ModelAdmin):
	list_display = ('boia', 'timestamp')

class TokenAdmin(admin.ModelAdmin):
	list_display = ('token', 'centre')

class SliderAdmin(admin.ModelAdmin):
	list_display = ('title',)

admin.site.register(Centre, CentreAdmin)
admin.site.register(Boia, BoiaAdmin)
admin.site.register(Registre_boia, RegistreBoiaAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Slider, SliderAdmin)