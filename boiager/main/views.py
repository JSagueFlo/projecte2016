import json
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, PwdChangeForm
from .functions import getUserCentres, getPublicCentres, check_centre, check_boia, token_validates, check_expired_tokens
from .models import Centre, Boia, Token, Slider



###################
## PÀGINES VIEWS ##
###################

def home(request):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	# Obtenir tots els sliders
	sliders = Slider.objects.all()
	context = {'sliders': sliders}
	return render(request, 'home.html', context)


def pagines(request, label):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	context = {'label': label}
	return render(request, 'pagines/'+ label + '.html', context)


################
## USER VIEWS ##
################

def signup(request):

	# Si l'usuari ja està autenticat redirigir al home
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		messages.add_message(request, messages.WARNING, "Ja estàs autenticat com a " + request.user.username + ".")
		return redirect('/')

	# Omplir el formulari amb les dades que arriven per POST o deixar-lo buit en cas que no hi hagi POST
	form = SignupForm(data=request.POST or None)
	token = ""

	# Si hi ha POST
	if request.method == 'POST':
		try:
			token = request.POST["token"]
			# Obtenir l'objecte token corresponent
			token_obj = Token.objects.get(token=token)
			# Si el token no està utilitzat
			if not token_obj.used:
				# Obtenir el centre al que pertany el token
				centre = token_obj.centre
				# Si el formulari és vàlid
				if form.is_valid():
					# Crear un usuari a partir de la informació del formulari
					new_user = form.save()
					# Si s'ha pogut crear l'usuari
					if new_user is not None:
						# Vincular l'usuari amb el centre
						centre.user.add(new_user)
						# Vincular l'usuari amb el token
						token_obj.use(new_user)
						# Si s'han acabat els tokens sense utilitzar del centre, generar-ne de nous
						if Token.objects.filter(centre=centre, used=0).count() == 0:
							centre.generate_tokens(10)
						# Autenticar el nou usuari
						new_user = authenticate( username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
						auth_login(request, new_user)
						messages.add_message(request, messages.SUCCESS, "Benvingut a Boiager!")
					return redirect('/')
			else:
				return redirect('/codi')
		except:
			return redirect('/codi')

	# Si hi ha GET
	if request.method == 'GET':
		try:
			token = request.GET["token"]
			# Si el token és vàlid
			if token_validates(token):
				# Canviar l'estat del token a being_used
				token_obj = Token.objects.get(token=token)
				token_obj.being_used = 1
				token_obj.save()
			else:
				messages.add_message(request, messages.ERROR, "El codi que has introduït és invàlid!")
				return redirect('/codi')
		except:
			return redirect('/codi')

	context = {'form': form, 'token': token}
	return render(request, 'signup.html', context)


def login(request):
	# Si l'usuari ja està autenticat redirigir al home
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		messages.add_message(request, messages.WARNING, "Ja estàs autenticat com a " + request.user.username + ".")
		return redirect('/')

	# Omplir el formulari amb les dades que arriven per POST o deixar-lo buit en cas que no hi hagi POST
	form = AuthenticationForm(data=request.POST or None)

	# Si hi ha POST
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Autenticar l'usuari amb les dades del formulari
		user = authenticate( username = username, password = password)
		# Si s'ha pogut autenticar i l'usuari està actiu (compte habilitat)
		if user is not None and user.is_active:
			# Logejar-se amb l'usuari
			auth_login(request, user)
			messages.add_message(request, messages.SUCCESS, "Benvingut a Boiager!")
			return redirect('/')

	context = {'form': form, }
	return render(request, 'login.html', context)


def change_password(request):

	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
		# Omplir el formulari amb les dades que arriven per POST o deixar-lo buit en cas que no hi hagi POST
		form = PwdChangeForm(user=request.user,data=request.POST or None)
		# Si hi ha POST
		if request.method == 'POST':
			old_password = request.POST['old_password']
			user = request.user
			# Si la contrasenya antiga és correcta
			if user.check_password(old_password):
				new_password1 = request.POST['new_password1']
				new_password2 = request.POST['new_password2']
				# Si els dos camps de contrasenya nova coincideixen
				if new_password1 == new_password2:
					# Modificar la contrasenya de l'usuari
					user.set_password(new_password1)
					user.save()
					user = authenticate(username=user.username, password=new_password1)
					auth_login(request, user)
					messages.add_message(request, messages.SUCCESS, "Contrasenya canviada amb èxit!")
					return redirect('/')
		context = {'form': form}
		return render(request, 'change_password.html', context)
	else:
		return redirect('/')


def logout(request):
	# Sortir del compte
	auth_logout(request)
	messages.add_message(request, messages.WARNING, "Adeu!")
	return redirect('/')


def codi(request):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	# Si hi ha GET
	if request.method == 'GET':
		# Si hi ha token en la petició
		if 'token' in request.GET.keys():
			try:
				token = request.GET["token"]
				# Si el token és vàlid
				if token_validates(token):
					# Obtenir l'objecte token
					token_obj = Token.objects.get(token=token)
					# Vincular l'usuari amb el token
					token_obj.use(request.user)
					centre = Centre.objects.get(token=token_obj)
					# Vincular l'usuari amb el centre
					centre.user.add(request.user)
					messages.add_message(request, messages.SUCCESS, centre.name + ' vinculat al teu compte amb èxit!')
					return redirect('/centres')
				else:
					messages.add_message(request, messages.ERROR, "El codi que has introduït és invàlid!")
					return redirect('/codi')
			except:
				return redirect('/codi')

	context = {}
	return render(request, 'codi.html', context)



#####################
## DASHBOARD VIEWS ##
#####################


def dashboard(request):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
		# Si hi ha GET
		if request.method == 'GET':
			# Si hi ha token en la petició
			if 'token' in request.GET.keys():
				try:
					token = request.GET["token"]
					# Si el token és vàlid
					if token_validates(token):
						# Obtenir l'objecte token
						token_obj = Token.objects.get(token=token)
						# Vincular l'usuari amb el token
						token_obj.use(request.user)
						centre = Centre.objects.get(token=token_obj)
						# Vincular l'usuari amb el centre
						centre.user.add(request.user)
						messages.add_message(request, messages.SUCCESS, centre.name + ' vinculat al teu compte amb èxit!')
						return redirect('/dashboard')
					else:
						messages.add_message(request, messages.ERROR, "El codi que has introduït és invàlid!")
						return redirect('/dashboard')
				except:
					messages.add_message(request, messages.ERROR, "Error intern! :(")
					return redirect('/dashboard')
		# Si hi ha POST
		elif request.method == 'POST':
			# Modificar les dades de l'usuari a partir de les dades del formulari
			request.user.first_name = request.POST['first_name']
			request.user.last_name = request.POST['last_name']
			request.user.email = request.POST['email']
			request.user.save()

		centres = Centre.objects.filter(user=request.user)
	else:
		return redirect('/')
	context = {'centres': centres}
	return render(request, 'dashboard.html', context)


def elimina_centre(request, centre_id):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		try:
			user = request.user
			# Obtenir l'objecte centre a partir de la id del centre
			centre = Centre.objects.get(pk=int(centre_id))
			# Desvincular el centre de l'usuari
			centre.user.remove(user)
			messages.add_message(request, messages.SUCCESS, centre.name + ' desvinculat del teu compte amb èxit!')
			return redirect('/dashboard')
		except:
			messages.add_message(request, messages.WARNING, 'Error al intentar desvincular el centre ' + centre.name)
			return redirect('/dashboard')
	else:
		return redirect('/')


def elimina_user(request):
	user = request.user
	# Sortir de la compte d'usuari
	auth_logout(request)
	# Deshabilitar el compte d'usuari
	user.is_active = 0
	user.save()
	return redirect('/')


##################
## CENTRE VIEWS ##
##################

def centres(request):
	centres_privats = None
	privats = []
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
		# Obtenir els centres privats de l'usuari
		centres_privats = getUserCentres(request)
		privats = serializers.serialize('json', centres_privats)
	# Obtenir els centres públics
	centres_publics = getPublicCentres()
	publics = serializers.serialize('json', centres_publics)
	
	context = {'centres_privats': centres_privats, 'centres_publics': centres_publics, 'privats': privats, 'publics': publics }

	return render(request, 'centres.html', context)


def centre(request, id_centre):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	# Comprobar l'existencia del centre i que l'usuari tingui accés a aquell centre
	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre

	# Obtenir les boies del centre
	boies = Boia.objects.filter(centre=centre)
	data = serializers.serialize('json', boies)
	# Obtenir les coordenades centrals del centre
	map_centre = centre.get_map_coords()
	context = {'centre': centre, 'boies': boies, 'data': data, 'map_centre': map_centre}
	return render(request, 'centre.html', context)


################
## BOIA VIEWS ##
################

def boia(request, id_centre, id_boia):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	# Comprobar l'existencia del centre i que l'usuari tingui accés a aquell centre
	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre
	# Comprobar l'existencia de la boia i que l'usuari tingui accés a aquella boia
	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		# Obtenir l'objecte boia
		boia = Boia.objects.get(pk=int(id_boia), centre=centre)
		# Obtenir els valors màxims i mínims de la boia en el dia d'avui
		max_min = boia.get_registres_max_min_today()
		# Obtenir l'últim registre de la boia
		latest = boia.get_registre_actual()
		# Obtenir les dates en les quals hi ha dades de la boia (menú de dates)
		dates = boia.get_dates()
		# Obtenir la primera i última data en les quals hi ha desdes de la boia (datepicker)
		min_data, max_data = boia.get_dates_min_max()
		# Obtenir els últims 10 registres de la boia (Chart)
		ultims_registres = serializers.serialize('json', boia.get_latest_registres())
	except:
		messages.add_message(request, messages.WARNING, "La boia a la que intentes accedir no existeix!")
		return redirect('/centre/' + str(centre.id) + '/')
	# Si és AJAX
	if request.is_ajax():
		# Retornar els últims 10 registres de la boia
		return JsonResponse(ultims_registres, safe=False)
	# Si no és AJAX
	else:
		# Retornar la template amb les dades corresponents
		context = {'centre': centre, 'boia': boia, 'max_min': max_min, 'latest': latest, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'ultims_registres': ultims_registres, 'sidebar': True}
		return render(request, 'boia.html', context)


def boia_any(request, id_centre, id_boia, year):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	# Comprobar l'existencia del centre i que l'usuari tingui accés a aquell centre
	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre
	# Comprobar l'existencia de la boia i que l'usuari tingui accés a aquella boia
	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		# Obtenir els valors mínims i màxims dels mesos de l'any de la boia
		max_min = boia.get_registres_max_min_avg(int(year))
		# Obtenir les dates en les quals hi ha dades de la boia (menú de dates)
		dates = boia.get_dates()
		# Si la boia no te dades per aquell any
		if not int(year) in dates.keys():
			# Redirigir al home
			return redirect('/')
		# Obtenir els valors de les mitjanes dels mesos de l'any de la boia
		mitjanes = json.dumps(boia.get_registres_anuals(int(year)))
		# Obtenir la primera i última data en les quals hi ha desdes de la boia (datepicker)
		min_data, max_data = boia.get_dates_min_max()
	except:
		return redirect('/')

	context = {'centre': centre, 'boia': boia, 'max_min': max_min, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'mitjanes': mitjanes, 'year': year, 'sidebar': True}

	return render(request, 'boia_chart.html', context)


def boia_mes(request, id_centre, id_boia, year, month):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	# Comprobar l'existencia del centre i que l'usuari tingui accés a aquell centre
	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre
	# Comprobar l'existencia de la boia i que l'usuari tingui accés a aquella boia
	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		# Obtenir els valors mínims i màxims dels dies del mes i any de la boia
		max_min = boia.get_registres_max_min_avg(int(year), int(month))
		# Obtenir les dates en les quals hi ha dades de la boia (menú de dates)
		dates = boia.get_dates()
		# Si la boia no té dades per aquell mes i any
		if not int(year) in dates.keys() or not int(month) in dates[int(year)].keys():
			# Redirigir al home
			return redirect('/')
		# Obtenir els valors de les mitjanes dels dies del mes i any de la boia
		mitjanes = json.dumps(boia.get_registres_mensuals(int(year), int(month)))
		# Obtenir la primera i última data en les quals hi ha desdes de la boia (datepicker)
		min_data, max_data = boia.get_dates_min_max()
	except:
		return redirect('/')


	context = {'centre': centre, 'boia': boia, 'max_min': max_min, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'mitjanes': mitjanes, 'year': year, 'month': month, 'sidebar': True}

	return render(request, 'boia_chart.html', context)


def boia_dia(request, id_centre, id_boia, year, month, day):
	# Si l'usuari està autenticat
	if request.user.is_authenticated and str(request.user) != 'AnonymousUser':
		# Comprobar la vigència dels tokens
		check_expired_tokens(request.user)
	# Comprobar l'existencia del centre i que l'usuari tingui accés a aquell centre
	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre
	# Comprobar l'existencia de la boia i que l'usuari tingui accés a aquella boia
	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		# Obtenir els valors mínims i màxims de les hores del dia, mes i any de la boia
		max_min = boia.get_registres_max_min_avg(int(year), int(month), int(day))
		# Obtenir les dates en les quals hi ha dades de la boia (menú de dates)
		dates = boia.get_dates()
		# Si la boia no té dades per aquell dia, mes i any
		if not int(year) in dates.keys() or not int(month) in dates[int(year)].keys() or not int(day) in dates[int(year)][int(month)].keys():
			# Redirigir al home
			return redirect('/')
		# Obtenir esl valors de les mitjanes de les hores del dia, mes i any de la boia
		mitjanes = json.dumps(boia.get_registres_diaris(int(year), int(month), int(day)))
		# Obtenir la primera i última data en les quals hi ha desdes de la boia (datepicker)
		min_data, max_data = boia.get_dates_min_max()
	except:
		return redirect('/')


	context = {'centre': centre, 'boia': boia, 'max_min': max_min, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'mitjanes': mitjanes, 'year': year, 'month': month, 'day': day, 'sidebar': True}

	return render(request, 'boia_chart.html', context)
