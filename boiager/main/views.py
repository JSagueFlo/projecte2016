import json
from django.core import serializers
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render_to_response, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import SignupForm
from .functions import getSliders, getUserCentres, getPublicCentres, check_centre, check_boia, token_validates
from .models import Centre, Slider, Boia, Token


#from django.shortcuts import get_object_or_404


################
## USER VIEWS ##
################

def home(request):
	sliders = getSliders()
	context = {'sliders': sliders}
	return render(request, 'home.html', context)


def signup(request):
	sliders = getSliders()
	form = SignupForm(data=request.POST or None)
	token = ""
	if request.method == 'POST':
		token = request.POST["token"]
		token_obj = Token.objects.get(token=token)
		centre = token_obj.centre
		if form.is_valid():
			new_user = form.save()
			if new_user is not None:
				centre.user.add(new_user)
				token_obj.being_used = 0
				token_obj.used = 1
				token_obj.save()
				new_user = authenticate( username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
				auth_login(request, new_user)
				messages.add_message(request, messages.SUCCESS, "Benvingut a Boiager!")
			return redirect('/')
	if request.method == 'GET':
		token = request.GET["token"]
		if token_validates(token):
			token_obj = Token.objects.get(token=token)
			token_obj.being_used = 1
			token_obj.save()
		else:
			messages.add_message(request, messages.ERROR, "El codi que has introduït és invàlid!")
			return redirect('/codi')
	context = {'form': form, 'sliders': sliders, 'token': token}
	return render(request, 'signup.html', context)


def login(request):
	sliders = getSliders()
	form = AuthenticationForm(data=request.POST or None)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate( username = username, password = password)
		if user is not None:
			auth_login(request, user)
			messages.add_message(request, messages.SUCCESS, "Benvingut a Boiager!")
			return redirect('/')

	context = {'form': form, 'sliders': sliders}
	return render(request, 'login.html', context)


def logout(request):
	auth_logout(request)
	messages.add_message(request, messages.WARNING, "Adeu!")
	return redirect('/')


def codi(request):
	sliders = getSliders()

	context = {'sliders': sliders}
	return render(request, 'codi.html', context)


##################
## CENTRE VIEWS ##
##################

def centres(request):
	sliders = getSliders()
	centres_privats = None
	privats = []

	if request.user.is_authenticated:
		centres_privats = getUserCentres(request)
		privats = serializers.serialize('json', centres_privats)
	centres_publics = getPublicCentres()
	publics = serializers.serialize('json', centres_publics)
	
	context = {'sliders': sliders, 'centres_privats': centres_privats, 'centres_publics': centres_publics, 'privats': privats, 'publics': publics }

	return render(request, 'centres.html', context)


def centre(request, id_centre):
	sliders = getSliders()
	# Centre exists?
	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre

	boies = Boia.objects.filter(centre=centre)
	data = serializers.serialize('json', boies)
	map_centre = centre.get_map_coords()
	context = {'sliders': sliders, 'centre': centre, 'boies': boies, 'data': data, 'map_centre': map_centre}
	return render(request, 'centre.html', context)


################
## BOIA VIEWS ##
################

def boia(request, id_centre, id_boia):
	sliders = getSliders()

	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre

	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		boia = Boia.objects.get(pk=int(id_boia), centre=centre)
		max_min = boia.get_registres_max_min_today()
		latest = boia.get_registre_actual()
		dates = boia.get_dates()
		min_data, max_data = boia.get_dates_min_max()
		ultims_registres = serializers.serialize('json', boia.get_latest_registres())
	except:
		messages.add_message(request, messages.WARNING, "La boia a la que intentes accedir no existeix!")
		return redirect('/centre/' + str(centre.id) + '/')

	if request.is_ajax():
		return JsonResponse(ultims_registres, safe=False)

	else:
		context = {'sliders': sliders, 'centre': centre, 'boia': boia, 'max_min': max_min, 'latest': latest, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'ultims_registres': ultims_registres, 'sidebar': True}
		return render(request, 'boia.html', context)


def boia_any(request, id_centre, id_boia, year):
	sliders = getSliders()

	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre

	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		max_min = boia.get_registres_max_min_avg(int(year))
		dates = boia.get_dates()
		if not int(year) in dates.keys():
			return redirect('/')
		mitjanes = json.dumps(boia.get_registres_anuals(int(year)))
		min_data, max_data = boia.get_dates_min_max()
	except:
		return redirect('/')

	context = {'sliders': sliders, 'centre': centre, 'boia': boia, 'max_min': max_min, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'mitjanes': mitjanes, 'year': year, 'sidebar': True}

	return render(request, 'boia_chart.html', context)


def boia_mes(request, id_centre, id_boia, year, month):
	sliders = getSliders()

	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre

	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		max_min = boia.get_registres_max_min_avg(int(year), int(month))
		dates = boia.get_dates()
		if not int(year) in dates.keys() or not int(month) in dates[int(year)].keys():
			return redirect('/')
		mitjanes = json.dumps(boia.get_registres_mensuals(int(year), int(month)))
		min_data, max_data = boia.get_dates_min_max()
	except:
		return redirect('/')


	context = {'sliders': sliders, 'centre': centre, 'boia': boia, 'max_min': max_min, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'mitjanes': mitjanes, 'year': year, 'month': month, 'sidebar': True}

	return render(request, 'boia_chart.html', context)


def boia_dia(request, id_centre, id_boia, year, month, day):
	sliders = getSliders()

	centre = check_centre(request, id_centre)
	if type(centre) is not Centre:
		return centre

	boia = check_boia(request, centre, id_boia)
	if type(boia) is not Boia:
		return boia

	try:
		max_min = boia.get_registres_max_min_avg(int(year), int(month), int(day))
		dates = boia.get_dates()
		if not int(year) in dates.keys() or not int(month) in dates[int(year)].keys() or not int(day) in dates[int(year)][int(month)].keys():
			return redirect('/')
		mitjanes = json.dumps(boia.get_registres_diaris(int(year), int(month), int(day)))
		min_data, max_data = boia.get_dates_min_max()
	except:
		return redirect('/')


	context = {'sliders': sliders, 'centre': centre, 'boia': boia, 'max_min': max_min, 'dates': dates, 'min_data': min_data, 'max_data': max_data, 'mitjanes': mitjanes, 'year': year, 'month': month, 'day': day, 'sidebar': True}

	return render(request, 'boia_chart.html', context)