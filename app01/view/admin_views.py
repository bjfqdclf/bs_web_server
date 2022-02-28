from django.shortcuts import render, HttpResponse, redirect


def home(request):
    return render(request, 'admin/admin_home.html')
