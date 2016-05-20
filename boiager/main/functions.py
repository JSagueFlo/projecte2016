from .models import Centre, Boia, Registre_boia, Token
from django.shortcuts import render_to_response, redirect, render
from django.contrib import messages
from django.utils import timezone



def getUserCentres(request):
	"""
	:param request: S'utilitza per agafar l'usuari
	:return: llista de centres privats de l'usuari
	"""
	if str(request.user) != 'AnonymousUser':
		return Centre.objects.filter(user=request.user, is_public=False)
	else:
		return


def getPublicCentres():
	"""
	:return: llista de centres públics
	"""
	return Centre.objects.filter(is_public=True)


def check_centre(request, id_centre):
	"""
	Comprova si un usuari té accés a un centre, si és així retorna el centre.
	:param request: S'utilitza per retornar missatges de notificació i per identificar l'usuari
	:param id_centre: id del centre a filtrar
	:return: un centre
	"""
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
	"""
	Comprova si una boia pertanya a un centre, si és així retorna la boia.
	:param request: S'utilitza per retornar missatges de notificació i per identificar l'usuari
	:param centre: S'ulitza per comprovar que una boia pertany a un centre
	:param id_boia: S'ulitza per comprovar que una boia pertany a un centre
	:return: una boia
	"""
	try:
		boia = Boia.objects.get(pk=int(id_boia), centre=centre)
		return boia
	except:
		messages.add_message(request, messages.WARNING, "La boia a la que intentes accedir no existeix!")
		return redirect('/centre/' + str(centre.id) + '/')

def token_validates(token):
	"""
	Comprova que un token existeixi i no estigui utilitzat
	:param token: s'utilitza per identificar un token
	:return: booleà
	"""
	try:
		Token.objects.get(token=token, used=0, being_used=0)
		return True
	except:
		return False


def check_expired_tokens(user):
	"""
	Comprova que els tokens d'un usuari estiguin vigents, si no ho estan elimina la relació entre centre i usuari corresponents.
	:param user: s'utilitza per identificar un usuari
	:return: void
	"""
	tokens = Token.objects.filter(user=user)
	for token in tokens:
		if token.expire_date <= timezone.now():
			centre = token.centre
			centre.user.remove(user)