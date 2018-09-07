# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from .models import VulRecord
from django.contrib.auth.decorators import login_required



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
        return HttpResponse('待审核')
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
            vuls_like = VulRecord.objects.filter(vul_url__contains=vul.vul_url)
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
        if request.user.is_staff:
            id = int(request.POST.get('id'))
            vul = VulRecord.objects.get(id=id)
            vul.vul_review = True
            vul.vul_review_people = request.user
            vul.vul_score = request.POST.get('score')
            vul.save()
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