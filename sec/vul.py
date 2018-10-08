# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from .models import VulRecord
from django.contrib.auth.decorators import login_required
from yarl import URL
from django.contrib.auth.models import User
from django.db.models import Count, Sum


@login_required
def vul_add(request):
    context = {}
    if request.method == "POST":
        vul = VulRecord()
        vul.vul_finder = request.user
        vul.vul_type = request.POST.get('type')
        vul.vul_payload = request.POST.get('payload')
        vul.vul_url = request.POST.get('url')
        vul.vul_process = request.POST.get('process')
        vul.vul_score = request.POST.get('score')
        vul.vul_fix = request.POST.get('fix')
        vul.vul_image = request.FILES['image']
        vul.save()
        return HttpResponseRedirect('/my_vul/')
    else:
        pass
    return render(request, 'vul_add.html', context)


@login_required
def vul_review(request):
    context = {}
    if request.GET.get('id'):
        if request.user.is_staff:
            vul = VulRecord.objects.get(id=request.GET.get('id'))
            context['vul'] = vul
            path = URL(vul.vul_url).path
            vuls_like = VulRecord.objects.filter(vul_url__contains=path, vul_review=True)
            context['vuls_like'] = vuls_like
            return render(request, 'one_vul.html', context)
        else:
            context = {
                'message': "只有管理员才能够访问",
                'url': "",
                'code': "history.go(-1);"
            }
            return render(request, 'error.html', context)
    else:
        vuls = VulRecord.objects.filter(vul_review=False)
        context['vuls'] = vuls
        return render(request, 'vul_review.html', context)


@login_required
def vul_reviewed(request):
    context = {}
    if request.POST.get('id'):
        # 审核通过漏洞
        if request.user.is_staff:
            id = int(request.POST.get('id'))
            vul = VulRecord.objects.get(id=id)
            vul.vul_review = True
            vul.vul_review_people = request.user
            vul.vul_score = request.POST.get('score')
            if request.POST.get('first'):
                vul.vul_frist = True
                vul.vul_score = vul.vul_score + 100
            print(request.POST.get('first'))
            vul.save()
        else:
            context = {
                'message': "只有管理员才能够访问",
                'url': "",
                'code': "history.go(-1);"
            }
            return render(request, 'error.html', context)
    if request.GET.get('id'):
        if request.user.is_staff:
            vul = VulRecord.objects.get(id=request.GET.get('id'))
            context['vul'] = vul
            path = URL(vul.vul_url).path
            vuls_like = VulRecord.objects.filter(vul_url__contains=path, vul_review=True)
            context['vuls_like'] = vuls_like
            return render(request, 'one_vul_reviewed.html', context)
        else:
            context = {
                'message': "只有管理员才能够访问",
                'url': "",
                'code': "history.go(-1);"
            }
            return render(request, 'error.html', context)
    vuls = VulRecord.objects.filter(vul_review=True)
    context['vuls'] = vuls
    return render(request, 'vul_review.html', context)


@login_required
def my_vul(request):
    context = {}
    vuls = VulRecord.objects.filter(vul_finder=request.user)
    score = 0
    for vul in vuls:
        if vul.vul_review:
            score = score + vul.vul_score
    context['vuls'] = vuls
    context['score'] = score
    return render(request, 'my_vul.html', context)


def ranking(request):
    context = {}
    vuls = VulRecord.objects.values("vul_finder__username").annotate(vul_score_sum=Sum("vul_score"),
                                                                     vul_score_count=Count("vul_score")).filter(
        vul_review=True).order_by("vul_score_sum")
    context['vuls'] = vuls
    return render(request, 'ranking.html', context)
