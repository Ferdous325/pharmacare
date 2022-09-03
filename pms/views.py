from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from pms.forms import SignUpForm


def index(request):
    if request.user.is_authenticated:
        return render(request, 'pms/index.html')
    else:
        return redirect('login')


def signout(request):
    logout(request)
    return redirect('login')


def signin(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'pms/login.html', context={'errors': "Invalid Credentials, Please try again!"})
    else:
        return render(request, 'pms/login.html')


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            # TODO add a flush message in login form
            return redirect('login')
        else:
            return render(request, 'pms/signup.html', context={'errors': signup_form.errors})
    return render(request, 'pms/signup.html')
