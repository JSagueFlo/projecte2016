from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import SignupForm
from django.template import RequestContext


#from django.shortcuts import get_object_or_404

def home(request):
	return render(request, 'home.html')


def signup(request):
	form = SignupForm(data=request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			return redirect('/')
	return render(request, 'signup.html', {'form': form})


def login(request):
	form = AuthenticationForm(data=request.POST or None)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate( username = username, password = password)
		if user is not None:
			auth_login(request, user)
			return redirect('/')

	return render(request, 'login.html', {'form': form})


def logout(request):
	auth_logout(request)
	return redirect('/')


def fail(request):
	return render(request, 'fail.html')