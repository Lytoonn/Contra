"""
See:
    https://docs.djangoproject.com/en/5.1/ref/contrib/auth/
    https://docs.djangoproject.com/en/5.1/ref/contrib/auth/#utility-functions
"""
from functools import wraps

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from common.django_utils import AsyncViewT

def aclient_required(client_view: AsyncViewT):
    @login_required(login_url = 'login')
    @wraps(client_view)
    async def fun(request: HttpRequest, *args, **kargs) -> HttpResponse:
        user = await aget_user(request)
        if user.is_authenticated and not user.is_writer:
            return await client_view(request, *args, **kargs)
        return HttpResponseForbidden("Only clients can access this view.")
    
    return fun

def awriter_required(writer_view: AsyncViewT):
    @login_required(login_url = 'login')
    @wraps(writer_view)
    async def fun(request: HttpRequest, *args, **kargs) -> HttpResponse:
        user = await aget_user(request)
        if user.is_authenticated and user.is_writer:
            return await writer_view(request, *args, **kargs)
        return HttpResponseForbidden("Only writers can access this view.")
    
    return fun

def ensure_for_current_user(model: type, *, id_in_url: str = 'id', redirect_if_missing: str):
    def decorator(view: AsyncViewT):
        async def async_view(request: HttpRequest, *args, **kargs) -> HttpResponse:
            obj_id = kargs[id_in_url]
            current_user = await aget_user(request)
            try:
                obj = await model.objects.aget(id = obj_id, user = current_user)
                del kargs[id_in_url]
                return await view(request, obj, *args, **kargs)
            except ObjectDoesNotExist:
                return redirect(redirect_if_missing)
        return async_view
    return decorator