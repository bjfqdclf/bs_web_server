from django.shortcuts import render, HttpResponse, redirect


def home(request):
    user = request.user
    return render(request, 'student/student_home.html', {'username': user.name})
