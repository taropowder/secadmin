# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from .models import  WeekLearn, WeekTask
from datetime import date
from math import ceil


def week_list(request):
    context = {}
    week = request.GET.get('id')
    if not week:
        delta = date.today() - date(2018, 10, 22)
        week = ceil(delta.days / 7)
    weeklearns = WeekLearn.objects.filter(learn_week=week).order_by("learn_time")
    context['weeklearns'] = weeklearns
    context['week'] = week
    return render(request, 'week_list.html', context)


def submit_week_learn(request):
    context = {}
    delta = date.today() - date(2018, 10, 22)
    now_week = ceil(delta.days / 7)
    if request.method == 'POST':
        weeklearn = WeekLearn()
        weeklearn.learner = request.user
        weeklearn.learn_image = request.FILES['image']
        weeklearn.learn_week = now_week
        weeklearn.save()
        return HttpResponseRedirect("/week_list")
    weeklearns = WeekLearn.objects.filter(learn_week=now_week).order_by("learn_time")
    i = 0
    submit = False
    for weeklearn in weeklearns:
        if weeklearn.learner == request.user:
            submit = True
            break
        i = i + 1
    if i <= 10:
        task = WeekTask.objects.get(task_week=now_week+1)
    elif not submit:
        task = WeekTask.objects.get(task_week=now_week)
    context['task'] = task
    return render(request, 'submit_week_learn.html', context)
