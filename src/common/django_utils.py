"""
Common django utilities used by several other packages and Django 
apps inside this project.
"""

__all__ = (
    'AsyncFormMixin',
    'AsyncModelFormMixin',
    'AsyncViewT',
    'arender',
    'alogout',
)

from typing import Protocol

from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import django.contrib.auth as auth

from asgiref.sync import sync_to_async


class AsyncViewT(Protocol):
    """
    Type definition for an asynchronous view.
    """
    async def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        ...

class AsyncFormMixin:

    @sync_to_async
    def ais_valid(self: forms.BaseForm):
        return self.is_valid()
    
    @sync_to_async
    def arender(self: forms.BaseForm):
        return self.render()

class AsyncModelFormMixin(AsyncFormMixin):
    
    @sync_to_async
    def asave(self: forms.BaseForm):
        return self.save()
    
async def arender(*render_args, **render_kargs) -> HttpResponse:
    
    @sync_to_async
    def sync_call_render() -> HttpResponse:
        return render(*render_args, **render_kargs)
    return await sync_call_render()

async def alogout(*render_args, **render_kargs):

    @sync_to_async
    def sync_call_logout():
        auth.logout(*render_args, **render_kargs)
    await sync_call_logout()

