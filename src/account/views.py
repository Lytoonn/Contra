from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

async def home(request: HttpResponse) -> HttpResponse:
    """ ... """
    return render(request, 'account/home.html', {'x': 33})

async def register(request: HttpResponse) -> HttpResponse:
    """ ... """
    return render(request, 'account/register.html')

async def login(request: HttpResponse) -> HttpResponse:
    """ ... """
    return render(request, 'account/login.html')
