from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.base_interface.general_functions import edit_password
import json

def home(request):
    user = request.user
    return render(request, 'admin/admin_home.html', {'username': user.name})


def add_user(request):
    user = request.user
    return render(request, 'admin/add_user.html', {'username': user.name})


def edit_passwd(request):
    user = request.user
    return render(request, 'admin/admin_edit_passwd.html', {'username': user.name, 'code': user.code})

