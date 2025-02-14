from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user

from common.auth import aclient_required

@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    """
    This is the client dashboard.
    """
    return render(request, 'client/dashboard.html')