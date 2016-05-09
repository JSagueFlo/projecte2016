from .models import Slider, Centre, Boia, Registre_boia

def getSliders():
	return Slider.objects.all()

def getUserCentres(request):
    return Centre.objects.filter(user=request.user, is_public=False)

def getPublicCentres():
    return Centre.objects.filter(is_public=True)