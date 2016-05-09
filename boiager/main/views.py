from django.core import serializers
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import SignupForm
from .functions import getSliders, getUserCentres, getPublicCentres
from .models import Centre, Slider, Boia

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
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			
			auth_login(request, user)
			return redirect('/')
	context = {'form': form, 'sliders': sliders}
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
			return redirect('/')
	context = {'form': form, 'sliders': sliders}
	return render(request, 'login.html', context)


def logout(request):
	auth_logout(request)
	return redirect('/')



##################
## CENTRE VIEWS ##
##################

def centres(request):
	sliders = getSliders()
	centres_privats = None
	if request.user.is_authenticated:
		centres_privats = getUserCentres(request)
	centres_publics = getPublicCentres()
	
	context = {'sliders': sliders, 'centres_privats': centres_privats, 'centres_publics': centres_publics}

	return render(request, 'centres.html', context)


def centre(request, id_centre):
	sliders = getSliders()
	# Centre exists?
	try:
		centre = Centre.objects.get(pk=int(id_centre))
	except:
		return redirect('/centres')

	if not centre.is_public:
		# User permission?
		try:
			Centre.objects.get(user=request.user)
		except:
			#TODO Show not permission message
			return redirect('/')

	boies = Boia.objects.filter(centre=centre)
	data = serializers.serialize('json', boies)
	map_centre = centre.get_map_coords()
	context = {'sliders': sliders, 'centre': centre, 'boies': boies, 'data': data, 'map_centre': map_centre}
	return render(request, 'centre.html', context)


def boia(request, id_centre, id_boia):
	sliders = getSliders()
	# Centre exists?
	try:
		centre = Centre.objects.get(pk=int(id_centre))
	except:
		return redirect('/centres')

	# Boia exists and centre has boia?
	try:
		boia = Boia.objects.get(pk=int(id_boia),centre=centre)
	except:
		return redirect('/centres/' + centre.id)

	# User is allowed to see centre?
	if not centre.is_public:
		try:
			Centre.objects.get(user=request.user)
		except:
			# TODO Show not permission message
			return redirect('/')

	context = {'sliders': sliders, 'centre': centre, 'boia': boia}
	return render(request, 'boia.html', context)