from django.shortcuts import render, HttpResponse, redirect


def home(request):
    user = request.user
    return render(request, 'student/student_home.html', {'username': user.username})


def edit_passwd(request):
    user = request.user
    return render(request, 'student/student_edit_passwd.html', {'username': user.username, 'code': user.code})

