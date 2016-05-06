from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext


#from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
	return render(request, 'home.html')

def signup(request):
	return render(request, 'home.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate( username = username, password = password)
		if user is not None:
			auth_login(request, user)
			#aixo peta for fuck sake
			return redirect('/', username=username)
		else:
			return redirect('/fail/')
	else:
		form = AuthenticationForm()
		return render(request, 'login.html', {'form': form})

def logout(request):
	logout(request)
	return redirect('home')

def fail(request):
	return render(request, 'fail.html')