from django.shortcuts import render, HttpResponse, redirect


def home(request):
    user = request.user
    return render(request, 'admin/admin_home.html', {'username': user.name})


def add_user(request):
    user = request.user
    return render(request, 'admin/add_user.html', {'username': user.name})
