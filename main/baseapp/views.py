from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib.auth import logout
from .models import *
from .forms import *


# Login form backend
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('feed')
    else:
        form = LoginForm()        
    return render(request, 'baseapp/login.html', {'form': form})


# Signup from backend
def signup(request):
   
    if request.method == 'POST':
        
        username = request.POST['username'] 
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        def is_valid_password(password1):
    # Check the length of the password (minimum 8 characters).
            if len(password1) < 8:
                return False

    # Check for at least one uppercase letter.
            if not any(char.isupper() for char in password1):
                return False

    # Check for at least one lowercase letter.
            if not any(char.islower() for char in password1):
                return False

    # Check for at least one digit.
            if not any(char.isdigit() for char in password1):
                return False

    # Check for at least one special character (e.g., !@#$%^&*()).
            if not re.search(r'[!@#$%^&*()]', password1):
                return False

    # All conditions passed; the password is valid.
            return True

    
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, f"The user already exist")
            elif User.objects.filter(email = email).exists():
                messages.error(request, f"The email already exist")
            elif is_valid_password(password1) == False:
                messages.error(request, f"The password is not so strong.")
            else:
                data = User.objects.create_user(username = username, email = email, password = password1)  
                data.save()
                return redirect('login')    
        else:
            messages.error(request, f"The passwords doesnt match.")
            return redirect('signup')

    return render(request, 'baseapp/signup.html') 



# def home(request):


#     return render(request, 'baseapp/home.html')

def feed(request):
    profile = UserProfile.objects.get(user=request.user)

    context = {
        'profile': profile,
    }

    return render(request, 'baseapp/feed.html', context)


def editprofile(request):

    profile = UserProfile.objects.get(user=request.user)
    


    context = {
        
        'profile':profile
        }

    return render(request, 'baseapp/editprofile.html',context)


def profileview(request):
    profile = UserProfile.objects.get(user=request.user)

    context = {
        'profile':profile
        }
    return render(request,  'baseapp/profileview.html',context)


def message(request):
    return render(request,"baseapp/message.html")


def notification(request):
    return render(request, 'baseapp/notification.html')


def search(request):
    return render(request, 'baseapp/search.html')


def discover(request):
    return render(request, 'baseapp/discover.html')


def settings(request):
    return render(request, 'baseapp/settings.html')
    
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')