from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponse
import ast
from billing.customer.models import Customer
from billing.networking.models import Router
from django.utils import timezone
from billing.helpers import is_mac, format_mac
from configuration.settings import radius_accounting_interval


def index(request):
    return render(request, "index.html")


def _set_online(login, online=True):
    try:
        Customer.objects.filter(login=login).update(online=online)
    except Exception as e:
        print("set_online error", e)
    try:
        Customer.objects.filter(last_online_login=login).update(online=online)
    except Exception as e:
        print("set_online error", e)


def _set_last_datetime(login):
    try:
        Customer.objects.filter(login=login).update(
            last_online_datetime=timezone.localtime())
    except Exception as e:
        print("set_last_datetime error", e)
    try:
        Customer.objects.filter(last_online_login=login).update(
            last_online_datetime=timezone.localtime())
    except Exception as e:
        print("set_last_datetime error", e)


def _set_last_ip(from_nas):
    try:
        Customer.objects.filter(
            login=from_nas['User-Name']).update(last_online_ip=from_nas['Framed-IP-Address'])
    except Exception as e:
        print("set_last_ip error", e)


def _set_last_router(from_nas):
    try:
        routers = Router.objects.filter(ip_address=from_nas['NAS-IP-Address'])
        if len(routers) == 1:
            Customer.objects.filter(
                login=from_nas['User-Name']).update(last_online_router=routers.first())
    except Exception as e:
        print("set_last_router error", e)


def _set_dhcp(login, is_dhcp):
    try:
        Customer.objects.filter(login=login).update(last_online_dhcp=is_dhcp)
    except Exception as e:
        print("accounting set_dhcp error", e)


def _set_last_login(login, raw_login):
    try:
        Customer.objects.filter(login=login).update(
            last_online_login=raw_login)
    except Exception as e:
        print("accounting set_last_login error", e)
    try:
        Customer.objects.filter(last_online_login=login).update(
            last_online_login=raw_login)
    except Exception as e:
        print("accounting set_last_login error", e)


@csrf_exempt
def radius_authorize(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] not in ('', '127.0.0.1'):
        return HttpResponseNotFound()
# NAS
    from_nas = dict(ast.literal_eval(request.body.decode("UTF-8")))
    if not 'User-Name' in from_nas.keys():
        return HttpResponseForbidden()
    nas_username = format_mac(
        from_nas['User-Name']) if is_mac(from_nas['User-Name']) else from_nas['User-Name']
# customer
    customers = Customer.objects.filter(login=nas_username)
    if len(customers) != 1:
        return HttpResponseForbidden()
    customer = customers.first()
    if not customer.active or customer.balance() < 0:
        return HttpResponseForbidden()
    radius_reply = {
        'Acct-Interim-Interval': str(radius_accounting_interval),
        'Mikrotik-Rate-Limit': f"{customer.upload_speed()}k/{customer.download_speed()}k",
    }
    radius_config = {
        'Cleartext-Password': customer.password,
    }

    # dhcp
    if 'User-Password' in from_nas.keys() and from_nas['User-Password'] == '' and customer.password == '':
        radius_config['Cleartext-Password'] = 'dhcp'

    if customer.ip_address:
        radius_reply['Framed-IP-Address'] = customer.ip_address
    response = {"reply": radius_reply, "config": radius_config}
    return JsonResponse(response)


@csrf_exempt
def radius_accounting(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] not in ('', '127.0.0.1'):
        return HttpResponseNotFound()
    from_nas = dict(ast.literal_eval(request.body.decode("UTF-8")))
    acct_type = from_nas['Acct-Status-Type'] if from_nas['Acct-Status-Type'] else ''
    if 'User-Name' in from_nas.keys() and from_nas['User-Name']:
        nas_username_raw = from_nas['User-Name']
        if is_mac(from_nas['User-Name']):
            nas_username = format_mac(from_nas['User-Name'])
        else:
            nas_username = from_nas['User-Name']
    else:
        nas_username_raw = nas_username = ''
    if acct_type.lower() in ('start', 'interim-update'):
        _set_online(nas_username)
    elif acct_type.lower() == 'stop':
        _set_online(nas_username, False)
    _set_last_datetime(nas_username)
    _set_last_ip(from_nas)
    _set_last_router(from_nas)
    _set_last_login(nas_username, nas_username_raw)

    # dhcp OR hotspot-login-by-mac
    if is_mac(nas_username) and ('Calling-Station-Id' not in from_nas.keys() or format_mac(from_nas['Calling-Station-Id']) != nas_username):
        _set_dhcp(nas_username, True)
    else:  # login is not mac OR Calling-Station-Id == User-Name
        _set_dhcp(nas_username, False)
    return HttpResponse()
