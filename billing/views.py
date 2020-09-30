from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


@csrf_exempt
def radius_authorize(request):
    print("auth request:", request)
    print("auth request meta remote addr:", request.META['REMOTE_ADDR'])
    return HttpResponse("auth\n")


@csrf_exempt
def radius_accounting(request):
    print("acct request:", request)
    return HttpResponse("acct\n")
