from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import django.contrib.auth as auth

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from common.django_utils import arender
from .models import CustomUser

async def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'account/home.html')

async def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if await form.ais_valid():
            await form.asave()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = { 'register_form': form }
    return await arender(request, 'account/register.html', context)

async def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data = request.POST)
        if await form.ais_valid():
            email = request.POST['username']
            passwd = request.POST['password']
            user: CustomUser | None = await auth.aauthenticate(
                request,
                username = email,
                password = passwd,
            )

            if user:
                await auth.alogin(request, user)
                msg = (
                    'Thanks for returning, Writer!' if user.is_writer else
                    'Welcome back, Client!'
                )

                return HttpResponse(msg)
    else:
        form = CustomAuthenticationForm()

    context = { 'login_form': form }
    return await arender(request, 'account/login.html', context)