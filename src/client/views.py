from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user

from client.models import Subscription
from writer.models import Article
from common.auth import aclient_required
from common.django_utils import arender

PlanChoices = Subscription.PlanChoices

@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    """
    This is the client dashboard.
    """
    user = await aget_user(request)
    try:
        subscription = await Subscription.objects.aget(user = user, is_active = True)
        plan = PlanChoices(subscription.plan)
        subscription_plan = plan.label
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
    try:
        subscription = await Subscription.objects.aget(user = user, is_active = True)
        has_subscription = True
        plan = PlanChoices(subscription.plan)
        if plan == PlanChoices.STANDARD:
            articles = Article.objects.filter(is_premium = False)
        else:
            articles = Article.objects.all()
    except ObjectDoesNotExist:
        has_subscription = False
        articles = []
    
    context = {'has_subscription': has_subscription, 'articles': articles}
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
async def create_subscription(request: HttpRequest, sub_id: str, plan: str) -> HttpResponse:
    """
    This is the client's subscription page.
    """
    plan_choice = PlanChoices(plan)
    user = await aget_user(request)
    await Subscription.objects.acreate(
        plan = plan_choice.value,
        cost = '3.00' if plan_choice == PlanChoices.STANDARD else '9.00',
        payment_provider_id = sub_id,
        is_active = True,
        user = user,
    )
    context = {'subscription_plan': plan_choice.label}
    return await arender(request, 'client/create-subscription.html', context)
