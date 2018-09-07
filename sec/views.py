# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Blog, CTF_learning, ON_DUTY, Book
from random import choice
import time, datetime


# Create your views here.
def home(request):
    context = {}
    weeks = Blog.objects.values('week')
    weekblogs = {}
    if weeks:
        now = weeks.last()['week']
        for w in range(1, now + 1):
            weekblogs[str(w)] = []
            blog = Blog.objects.filter(week=w)
            if blog.count() <= 5:
                m = blog.count()
            else:
                m = 5
            for b in range(0, m):
                weekblogs[str(w)].append(blog[b])
    a = sorted(weekblogs.items(), key=lambda d: d[0])
    context['weekblogs'] = a
    return render(request, 'index.html', context)


@login_required
def submit(request):
    context = {}
    context['statu'] = '0'
    if request.method == 'POST':
        content = request.POST.get('content')
        url = request.POST.get('url')
        direction = request.POST.get('direction')
        weeks = datetime.datetime.now().isocalendar()
        week = weeks[1] - 11
        blog = Blog()
        blog.blog_user = User.objects.get(username=request.session['username'])
        blog.content = content
        blog.url = url
        blog.direction = direction
        blog.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        blog.week = week
        blog.save()
        context['statu'] = '1'
        context['error'] = "提交成功"
        return HttpResponseRedirect('/blog/' + str(week) + '/')
    return render(request, 'submit.html', context)


def user_login(request):
    context = {}
    context['statu'] = '0'
    if request.method == 'POST':
        get_name = request.POST.get('username')
        get_password = request.POST.get('password')
        user = authenticate(username=get_name, password=get_password)
        if user is not None:
            if user.is_active:
                request.session['username'] = get_name
                context['name'] = get_name
                request.session['id'] = user.id
                login(request, user)  # 这才是登录，才会写入session
                return HttpResponseRedirect('/')
            else:
                context['statu'] = '1'
                context['error'] = "您的用户已经被限制,请联系工作人员"
        else:
            context['statu'] = '1'
            context['error'] = "用户名或者密码错误"
    return render(request, 'login.html', context)


def register(request):
    context = {}
    context['statu'] = 0
    if request.method == 'POST':
        name = request.POST.get('name')
        u = User.objects.filter(username=name)
        if u:
            context['statu'] = 1
            context['error'] = '该名字已被使用'
            return render(request, 'register.html', context)
        password = request.POST.get('password')
        email = request.POST.get('eamil')
        user = User.objects.create_user(name, email, password)
        user.first_name = request.POST.get('firstname')
        user.save()
        context['name'] = name
        return render(request, 'login.html', context)
    return render(request, 'register.html', context)


def weekblog(request, week):
    context = {}
    blogs = Blog.objects.filter(week=week)
    context['blogs'] = blogs
    context['week'] = week
    u = User.objects.values('id')
    man = choice(u)
    context['man'] = man['id']
    return render(request, 'weekblog.html', context)


def myblog(request, user_id):
    context = {}
    blogs = Blog.objects.filter(blog_user_id=user_id)
    context['blogs'] = blogs
    return render(request, 'myblog.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def ctflerning(request):
    context = {}
    context['ctf'] = CTF_learning.objects.order_by('type')
    return render(request, 'ctflerning.html', context)


def changeblog(request):
    context = {}
    user_id = request.session['id']
    blogs = Blog.objects.filter(blog_user_id=user_id)
    context['blogs'] = blogs
    return render(request, 'changemyblog.html', context)


def change(request, change_id):
    if request.method == 'POST':
        blog = Blog.objects.filter(id=change_id)
        if blog.values('blog_user_id')[0]['blog_user_id'] == request.session['id']:
            content = request.POST.get('content')
            url = request.POST.get('url')
            Blog.objects.filter(id=change_id).update(content=content, url=url)
            return HttpResponseRedirect('/myblog/' + str(request.session['id']) + '/')
    return HttpResponseRedirect('/changeblog/')


def search(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        blogs = Blog.objects.filter(content__contains=name)
        context['blogs'] = blogs
    return render(request, 'search.html', context)


def classification(request):
    context = {}
    if request.method == 'POST':
        direction = request.POST.get('direction')
        blogs = Blog.objects.filter(direction=direction)
        context['blogs'] = blogs
    return render(request, 'classification.html', context)


def onduty(request):
    context = {}
    WEEK = ['Mon', 'Tue', 'Wed', 'Tur', 'Fri', 'Sat', 'Sun']
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.session['username'])
            name = user.first_name
        except:
            name = request.POST.get('name')
        if name != '':
            for y in WEEK:
                for x in range(1, 7):
                    weektime = y + str(x)
                    # print request.POST.get(weektime)
                    if request.POST.get(weektime) == 'on':
                        # print weektime
                        oldpeople = ON_DUTY.objects.filter(time=weektime)
                        if oldpeople:
                            if name not in oldpeople[0].name:
                                ON_DUTY.objects.update_or_create(time=weektime,
                                                                 defaults={'name': name + ',' + oldpeople[0].name})
                        else:
                            ON_DUTY.objects.update_or_create(time=weektime, defaults={'name': name})
    dutys = {}
    for y in WEEK:
        dutys[y] = []
        for x in range(1, 6):
            weektime = y + str(x)
            people = ON_DUTY.objects.filter(time=weektime)
            if people:
                # print people[0].name
                dutys[y].append(people[0].name)
            else:
                dutys[y].append('无')
        # print dutys[y]
    # print dutys
    duty = {}
    duty['Mon'] = dutys['Mon']
    context['duty'] = dutys
    context['conut'] = WEEK
    # print request.POST.get('Mon1')
    return render(request, 'onduty.html', context)


def book(request):
    context = {}
    context['books'] = Book.objects.all()
    return render(request, 'book.html', context)


@login_required
def lend(request):
    book = Book.objects.get(id=request.GET.get('id'))
    if book.is_lend == False:
        Book.objects.filter(id=request.GET.get('id')).update(lend_people_id=request.session['id'],
                                                             lend_time=datetime.datetime.now(), is_lend=True)
    return HttpResponseRedirect('/book/')


@login_required
def back(request):
    book = Book.objects.get(id=request.GET.get('id'))
    if request.session['id'] == book.lend_people_id:
        Book.objects.filter(id=request.GET.get('id')).update(lend_people_id=None, lend_time=None, is_lend=False)
    return HttpResponseRedirect('/book/')
