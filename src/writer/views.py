from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user

from .forms import ArticleForm
from common.auth import awriter_required
from common.django_utils import arender

@awriter_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    """
    This is the writer's dashboard.
    """
    return await arender(request, 'writer/dashboard.html')

@awriter_required
async def create_article(request: HttpRequest) -> HttpResponse:
    """
    This is the writer's create article.
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if await form.ais_valid():
            article = await form.asave(commit = False)
            article.user = await aget_user(request)
            await article.asave()
            return HttpResponse('Article created')
    else:
        form = ArticleForm()

    context = {'create_article_form': form}
    return await arender(request, 'writer/create-article.html', context)

@awriter_required
async def my_articles(request: HttpRequest) -> HttpResponse:
    """
    This is the writer's articles.
    """
    return await arender(request, 'writer/my-articles.html')

@awriter_required
async def account_settings(request: HttpRequest) -> HttpResponse:
    """
    This is the writer's account settings.
    """
    return await arender(request, 'writer/account-settings.html')

