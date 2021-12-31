from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth


def my_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=pwd)
        if user:
            auth.login(request, user)
            request.session.set_expiry(129600)  # 3天
            next_url = request.GET.get('next_path', '/test/')
            return redirect(next_url)
        else:
            print('login false...')

    return render(request, 'login.html')


def url_404(request):

    return render(request, 'ok')


def test(request):
    from app01.interface.admin_interface.user_operation import students_code_generate
    code = students_code_generate(1, 1)
    return HttpResponse(code) if code else HttpResponse('false')


def test2(request):
    return HttpResponse('test2')
