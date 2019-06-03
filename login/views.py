from django.shortcuts import render
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import reverse


def login(request):

    context = {}

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('qrcodes:newqr'))
        else:
            context = {
                'error': 'Wrong username or password.'
            }

    return render(request, 'login/login.html', context)


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('login:login'))


def signup(request):
    pass