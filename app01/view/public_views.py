from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth, messages


def all_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=pwd)
        if user:
            auth.login(request, user)
            request.session.set_expiry(129600)  # 3天
            next_url = request.GET.get('next_path', '/login/')
            if next_url is "/login/":
                if user.user_type == 1:
                    return redirect('/admin/home')
                elif user.user_type == 2:
                    return redirect('/teacher/home')
                else:
                    return redirect('/student/home')
            return redirect(next_url)
        else:

            messages.error(request, '用户名或密码不正确')

            return render(request, 'index.html')
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == 1:
            return redirect('/admin/home')
        elif user.user_type == 2:
            return redirect('/teacher/home')
        else:
            return redirect('/student/home')

    return render(request, 'index.html')


def logout(request):
    """退出账户"""
    request.session.flush()
    return render(request, 'index.html')


def url_404(request):

    return render(request, 'ok')


def test(request):
    from app01.interface.admin_interface.user_operation import students_code_generate
    code = students_code_generate(1, 1)
    return HttpResponse(code) if code else HttpResponse('false')


def test2(request):
    return HttpResponse('test2')
