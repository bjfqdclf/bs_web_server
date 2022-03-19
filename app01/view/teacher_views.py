from django.shortcuts import render, HttpResponse, redirect


def home(request):
    user = request.user
    return render(request, 'teacher/teacher_home.html', {'username': user.username})


def edit_passwd(request):
    user = request.user
    return render(request, 'teacher/teacher_edit_passwd.html', {'username': user.username, 'code': user.code})
