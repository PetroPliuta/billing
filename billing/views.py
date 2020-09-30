from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
import ast
from billing.customer.models import Customer


def index(request):
    return render(request, "index.html")


@csrf_exempt
def radius_authorize(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] not in ('', '127.0.0.1'):
        return HttpResponseNotFound()
# NAS
    from_nas = dict(ast.literal_eval(request.body.decode("UTF-8")))
    nas_username = ''
    if not 'User-Name' in from_nas.keys():
        return HttpResponseForbidden()
    nas_username = from_nas['User-Name']
# customer
    customers = Customer.objects.filter(login=nas_username)
    if len(customers) != 1:
        return HttpResponseForbidden()
    customer = customers.first()
    if not customer.active or customer.balance() < 0:
        return HttpResponseForbidden()
    radius_reply = {
        'Acct-Interim-Interval': '60',
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


@ csrf_exempt
def radius_accounting(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] not in ('', '127.0.0.1'):
        return HttpResponseNotFound()
    dict_str = request.body.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    return JsonResponse(mydata)
