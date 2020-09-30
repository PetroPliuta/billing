from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
import ast


def index(request):
    return render(request, "index.html")


@csrf_exempt
def radius_authorize(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] not in ('', '127.0.0.1'):
        return HttpResponseNotFound()
    # print("auth request:", request)
    # print("auth request meta remote addr:", request.META['REMOTE_ADDR'])
    # print(f"scheme: {request.scheme}")
    # print(request.POST.dict())
    # print(request.GET.dict())
    print(f"request.body: type-'{type(request.body)}': '{request.body}'")

    dict_str = request.body.decode("UTF-8")
    print(f"dict_str: type-'{type(dict_str)}': '{dict_str}'")

    mydata = ast.literal_eval(dict_str)
    print(f"mydata: type-'{type(mydata)}': '{mydata}'")

    # return HttpResponse(request.body)
    # return HttpResponse(request.POST.lists())

    dict_ = dict(mydata)
    # return HttpResponse(dict_)
    return JsonResponse(dict_)


@csrf_exempt
def radius_accounting(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] not in ('', '127.0.0.1'):
        return HttpResponseNotFound()
    dict_str = request.body.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    return JsonResponse(mydata)
