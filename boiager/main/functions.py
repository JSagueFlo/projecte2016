from .models import Slider, Centre, Boia, Registre_boia
from django.shortcuts import render_to_response, redirect, render
from django.contrib import messages

def getSliders():
	return Slider.objects.all()

def getUserCentres(request):
	if str(request.user) != 'AnonymousUser':
		return Centre.objects.filter(user=request.user, is_public=False)
	else:
		return

def getPublicCentres():
    return Centre.objects.filter(is_public=True)

def check_centre(request, id_centre):
	try:
		centre = Centre.objects.get(pk=int(id_centre))
	except:
		messages.add_message(request, messages.WARNING, "El centre al que intentes accedir no existeix!")
		return redirect('/centres')

	if not centre.is_public:
		# User permission?
		try:
			Centre.objects.filter(user=request.user)
		except:
			messages.add_message(request, messages.WARNING, "No tens permís per accedir a aquest centre!")
			return redirect('/centres')
	return centre

def check_boia(request, centre, id_boia):
	try:
		boia = Boia.objects.get(pk=int(id_boia), centre=centre)
	except:
		messages.add_message(request, messages.WARNING, "La boia a la que intentes accedir no existeix!")
		return redirect('/centre/' + str(centre.id) + '/')
	return boia