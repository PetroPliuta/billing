from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
import ast


def index(request):
    return render(request, "index.html")


@csrf_exempt
def radius_authorize(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] not in ('', '127.0.0.1'):
        return HttpResponseBadRequest()
    print("auth request:", request)
    print("auth request meta remote addr:", request.META['REMOTE_ADDR'])
    print(f"scheme: {request.scheme}")
    # print(request.POST.dict())
    # print(request.GET.dict())
    print(request.body)

    dict_str = request.body.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    # return HttpResponse(request.body)
    # return HttpResponse(request.POST.lists())

    return JsonResponse(mydata)


@csrf_exempt
def radius_accounting(request):
    print("acct request:", request)
    return HttpResponse("acct\n")
