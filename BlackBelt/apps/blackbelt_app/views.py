from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import User, UserManager
import bcrypt
  # the index function is called when root is visited
def index(request):
    return render(request, 'blackbelt/index.html')

def process(request):
    
    if request.method == 'POST':
        if request.POST['action'] == 'register':
            errors = User.objects.basic_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            else:
                hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'].lower(), password = hash1, birthday = request.POST['birthday'])
                return redirect ('/success')
        if request.POST['action'] == 'login':
            errors = User.objects.login_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
                
        return redirect('/success')


def success(request):


    return render(request, 'blackbelt/success.html')

