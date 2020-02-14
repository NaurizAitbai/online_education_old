from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'app_base/index.html')


def auth(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('projects:list')
        return render(request, 'app_base/auth.html')
    else:
        return render(request, 'app_base/auth.html')


def user_logout(request):
    logout(request)
    return redirect('index')