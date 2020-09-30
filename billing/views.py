from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse


def index(request):
    return render(request, "index.html")


@csrf_exempt
def radius_authorize(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    print("auth request:", request)
    print("auth request meta remote addr:", request.META['REMOTE_ADDR'])
    print(f"scheme: {request.scheme}")
    data = {
        "data": "post data",
        "scheme": request.scheme,
    }
    return JsonResponse(data)


@csrf_exempt
def radius_accounting(request):
    print("acct request:", request)
    return HttpResponse("acct\n")
