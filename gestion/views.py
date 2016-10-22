# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.template import RequestContext
from gestion.forms import LoginForm
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    message = None
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)        
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    message = 'El logueo de la sesión ha sido satisfactorio'
                    return render(request, 'home.html',{'message':message,'form':form})
                else:
                    message = 'Su usuario se encuentra inactivo'
            else:
                message = 'Nombre de usuario y/o contraseña incorrecto'
        else:
            form = LoginForm()
    return render(request, 'login.html', {'message': message, 'form': form})


def home_page(request):
    return render(request, 'homepage.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')
