# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import sec
from .models import WeekLearn, WeekTask
from datetime import date
from math import ceil


@login_required
def week_list(request):
    context = {}
    try:
        user_direction = request.user.userprofile.direction
    except Exception:
        user_direction = "sec"
    week = request.GET.get('id')
    if not week:
        delta = date.today() - date(2018, 10, 21)
        week = ceil(delta.days / 7)
    weeklearns = WeekLearn.objects.filter(learn_task__task_week=week, learn_task__task_direction=user_direction).order_by("learn_time")
    context['weeklearns'] = weeklearns
    context['week'] = week
    return render(request, 'week_list.html', context)


@login_required
def submit_week_learn(request):
    context = {}
    delta = date.today() - date(2018, 10, 21)
    now_week = ceil(delta.days / 7)
    try:
        user_direction = request.user.userprofile.direction
    except Exception:
        user_direction = "sec"
    weeklearns = WeekLearn.objects.filter(learn_task__task_week=now_week, learner=request.user)
    try:
        if weeklearns:
            task = WeekTask.objects.get(task_week=now_week + 1, task_direction=user_direction)
        else:
            task = WeekTask.objects.get(task_week=now_week, task_direction=user_direction)
    except Exception as e:
        print(e)
        context['error'] = "alert('请联系你懒惰的管理员添加任务吧！！');"
        return render(request, 'submit_week_learn.html', context)

    if request.method == 'POST':
        try:
            task = WeekTask.objects.get(task_week=now_week, task_direction=user_direction)
            weeklearn = WeekLearn()
            weeklearn.learner = request.user
            weeklearn.learn_image = request.FILES['image']
            weeklearn.learn_task = task
            weeklearn.save()
            return HttpResponseRedirect("/week_list")
        except Exception:
            context['error'] = "alert('未选择图片');"


    context['task'] = task
    return render(request, 'submit_week_learn.html', context)
