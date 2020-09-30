from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, "index.html")


def radius_authorize(request):
    print("auth request:", request)
    print("auth request meta remote addr:", request.META['REMOTE_ADDR'])
    return HttpResponse("auth\n")


def radius_accounting(request):
    print("acct request:", request)
    return HttpResponse("acct\n")
