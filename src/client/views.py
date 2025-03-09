from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from django.utils.translation import gettext as _t

from client.models import Subscription, PlanChoice
from .forms import UpdateSubscriptionForm
from writer.models import Article
from common.auth import aclient_required, ensure_for_current_user
from common.django_utils import arender
from . import paypal as sub_manager


@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    """
    This is the client dashboard.
    """
    user = await aget_user(request)
    subscription_plan = 'No subscription yet.'
    if subscription := await Subscription.afor_user(user):
        subscription_plan = (await subscription.aplan_choice()).name
        if not subscription.is_active:
            subscription_plan += ' (inactive)'

    context = {'subscription_plan': subscription_plan}
    return await arender(request, 'client/dashboard.html', context)

@aclient_required
async def browse_articles(request: HttpRequest) -> HttpResponse:
    """
    This is the client's page to browse articles.
    """
    user = await aget_user(request)
    articles = []
    if subscription := await Subscription.afor_user(user):
        if not await subscription.ais_premium():
            articles = Article.objects.filter(is_premium = False)
        else:
            articles = Article.objects.all()
    
    context = {'has_subscription': subscription is not None, 'articles': articles}
    return await arender(request, 'client/browse-articles.html', context)

@aclient_required
async def subscribe_plan(request: HttpRequest) -> HttpResponse:
    """
    This is the client's page to subscription plans.
    """
    user = await aget_user(request)
    if await Subscription.afor_user(user):
        return redirect('client-dashboard')
    
    context = {'plan_choices': PlanChoice.objects.filter(is_active = True)}
    return await arender(request, 'client/subscribe-plan.html', context)

@aclient_required
async def update_user(request: HttpRequest) -> HttpResponse:
    """
    This is the client's update account page.
    """
    user = await aget_user(request)
    subscription_plan = ''
    if subscription := await Subscription.afor_user(user):
        subscription_plan = (await subscription.aplan_choice()).name
    context = {
        'has_subscription': bool(subscription),
        'subscription': subscription,
        'subscription_plan': subscription_plan,
    }
    return await arender(request, 'client/update-user.html', context)


@aclient_required
async def create_subscription(request: HttpRequest, sub_id: str, plan_code: str) -> HttpResponse:
    """
    This is the client's subscription page.
    """
    user = await aget_user(request)

    if await Subscription.afor_user(user):
        return redirect('client-dashboard')

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

@aclient_required
@ensure_for_current_user(Subscription, redirect_if_missing = 'client-dashboard')
async def cancel_subscription(request: HttpRequest, subscription: Subscription) -> HttpResponse:
    """
    This is the client's cancel subscription page.
    """
    if request.method == 'POST':
        # First, cancel the subscription on PayPal
        access_token = await sub_manager.get_access_token()
        sub_id = subscription.external_subscription_id
        await sub_manager.cancel_subscription(access_token, sub_id)
        
        # Then, cancel it locally by removing it from the DB
        await subscription.adelete()

        # Set the template that confirms that the subscription was cancelled
        context = {}
        template = 'client/cancel-subscription-confirmed.html'

    else:
        context = {'subscription_plan': (await subscription.aplan_choice()).name}
        template = 'client/cancel-subscription.html'
    
    return await arender(request, template, context)

@aclient_required
@ensure_for_current_user(Subscription, redirect_if_missing = 'client-dashboard')
async def update_subscription(request: HttpRequest, subscription: Subscription) -> HttpResponse:
    """
    This is the client's update subscription page.
    """
    user_plan_choice = await subscription.aplan_choice()
    if request.method == 'POST':
        http_response = redirect('client-update-user')

    else:
        form = await UpdateSubscriptionForm.ainit(
            exclude = [user_plan_choice.plan_code],
            format_fn = lambda pc: _t(f'{pc.name} ({pc.cost}€ / month)')
        )
        context = {'update_subscription_form': form}
        http_response = await arender(request, 'client/update-subscription.html', context)

    return http_response