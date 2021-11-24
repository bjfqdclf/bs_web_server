from django.shortcuts import render, HttpResponse
from templates import *
# Create your views here.


def index(request):

    return render(request, 'index.html')


def test(request):
    return HttpResponse('ok')