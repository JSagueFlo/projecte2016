from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext


#from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
	return render_to_response('home.html')

def signup(request):
	return render_to_response('home.html')

def login(request):
	if request.method == 'POST':
		user = request.POST['username']
		password = request.POST['password']
		user = authenticate( user = user, password = password)
		if user is not None:
			return redirect('home')
		else:
			return redirect('fail')
	else:
		form = AuthenticationForm()

	return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

def logout(request):
	logout(request)
	return redirect('home')

def fail(request):
	return render_to_response('fail.html')