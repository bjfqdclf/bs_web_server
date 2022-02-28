from django.shortcuts import render, Http404


def code_401(request):
    """未授权"""
    return Http404


def code_404(request):
    """未找到"""
    return render(request, '')
