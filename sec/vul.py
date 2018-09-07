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
        vul.vul_url = request.POST.get('url')
        vul.vul_process = request.POST.get('process')
        vul.vul_score = request.POST.get('score')
        vul.vul_image = request.FILES['image']
        vul.save()
        print(request.FILES)
        return HttpResponse('待审核')
    else:
        pass
    return render(request, 'vul_add.html', context)

@login_required
def vul_review(request):
    context = {}
    vuls = VulRecord.objects.filter(vul_review=False)
    context['vuls'] = vuls
    return render(request, 'vul_review.html', context)