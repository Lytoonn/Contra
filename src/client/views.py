from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user

from client.models import Subscription, PlanChoice
from writer.models import Article
from common.auth import aclient_required
from common.django_utils import arender


@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    """
    This is the client dashboard.
    """
    user = await aget_user(request)
    try:
        subscription = await Subscription.objects.aget(user = user, is_active = True)
        subscription_plan = (await subscription.aplan_choice()).name
    except ObjectDoesNotExist:
        subscription_plan = 'No subscription yet.'
    context = {'subscription_plan': subscription_plan}
    return await arender(request, 'client/dashboard.html', context)

@aclient_required
async def browse_articles(request: HttpRequest) -> HttpResponse:
    """
    This is the client's page to browse articles.
    """
    user = await aget_user(request)
    subscription = None
    try:
        subscription = await Subscription.objects.aget(user = user, is_active = True)
        if not await subscription.ais_premium():
            articles = Article.objects.filter(is_premium = False)
        else:
            articles = Article.objects.all()
    except ObjectDoesNotExist:
        articles = []
    
    context = {'has_subscription': subscription is not None, 'articles': articles}
    return await arender(request, 'client/browse-articles.html', context)

@aclient_required
async def subscribe_plan(request: HttpRequest) -> HttpResponse:
    """
    This is the client's page to subscription plans.
    """
    return await arender(request, 'client/subscribe-plan.html')

@aclient_required
async def update_user(request: HttpRequest) -> HttpResponse:
    """
    This is the client's update account page.
    """
    user = await aget_user(request)
    subscription = None
    try:
        subscription = await Subscription.objects.aget(user = user, is_active = True)
    except ObjectDoesNotExist:
        pass
    context = {'has_subscription': subscription is not None}
    return await arender(request, 'client/update-user.html', context)


@aclient_required
async def create_subscription(request: HttpRequest, sub_id: str, plan_code: str) -> HttpResponse:
    """
    This is the client's subscription page.
    """
    user = await aget_user(request)
    plan_choice = await PlanChoice.afrom_plan_code(plan_code)
    await Subscription.objects.acreate(
        plan_choice = plan_choice,
        cost = plan_choice.cost,
        external_subscription_id = sub_id,
        is_active = True,
        user = user,
    )
    context = {'subscription_plan': plan_choice.name}
    return await arender(request, 'client/create-subscription.html', context)
