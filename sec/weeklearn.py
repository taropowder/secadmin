# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import WeekLearn, WeekTask
from datetime import date
from math import ceil


@login_required
def week_list(request):
    context = {}
    week = request.GET.get('id')
    if not week:
        delta = date.today() - date(2018, 10, 21)
        week = ceil(delta.days / 7)
    weeklearns = WeekLearn.objects.filter(learn_week=week).order_by("learn_time")
    context['weeklearns'] = weeklearns
    context['week'] = week
    return render(request, 'week_list.html', context)


@login_required
def submit_week_learn(request):
    context = {}
    delta = date.today() - date(2018, 10, 21)
    now_week = ceil(delta.days / 7)
    if request.method == 'POST':
        try:

            weeklearn = WeekLearn()
            weeklearn.learner = request.user
            weeklearn.learn_image = request.FILES['image']
            weeklearn.learn_week = now_week
            weeklearn.save()
            return HttpResponseRedirect("/week_list")
        except Exception:
            context['error'] = "alert('未选择图片');"
    weeklearns = WeekLearn.objects.filter(learn_week=now_week).order_by("learn_time")
    i = 0
    submit = False
    for weeklearn in weeklearns:
        if weeklearn.learner == request.user:
            submit = True
            break
        i = i + 1
    if i <= 10 and submit:
        task = WeekTask.objects.get(task_week=now_week + 1)
    elif not submit:
        task = WeekTask.objects.get(task_week=now_week)
    context['task'] = task
    return render(request, 'submit_week_learn.html', context)
