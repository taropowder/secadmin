# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    blog_user = models.ForeignKey(User)
    content = models.TextField(null=False)
    direction = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField()

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.content
    class Meta:
        ordering = ["time"]


class CTF_learning(models.Model):
    title = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    type = models.CharField(max_length=20)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.title


class ON_DUTY(models.Model):
    time = models.CharField(max_length=30)
    name = models.CharField(max_length=100)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.time


class Book(models.Model):
    TYPE_CHOICES = (
        ('web', '网络'),
        ('re', '逆向'),
        ('program', '开发'),
        ('system', '系统'),
        ('other', '其他'),
    )
    name = models.CharField(max_length=30)
    storage_time = models.DateTimeField(auto_now_add=True)
    lend_time = models.DateTimeField(null=True, blank=True)
    lend_people = models.ForeignKey(User, null=True, blank=True)
    is_lend = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='bookimages/%Y/%m', verbose_name='缩略图', null=True, blank=True)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name


class VulRecord(models.Model):
    TYPE_CHOICES = (
        ('sql', 'SQL注入'),
        ('xss', 'XSS'),
        ('upload', '文件上传'),
        ('shell', '命令执行'),
        ('ssrf', 'SSRF'),
        ('csrf', 'CSRF'),
        ('code', '代码注入'),
        ('delete', '任意删除'),
        ('download', '任意下载'),
        ('logic', '逻辑漏洞'),
        ('unacc', '未授权访问'),
    )
    vul_finder = models.ForeignKey(User, related_name="finder")
    vul_url = models.CharField(max_length=100)
    vul_payload = models.TextField(null=True)
    vul_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    vul_process = models.TextField()
    vul_score = models.IntegerField()
    vul_review = models.BooleanField(default=False)
    vul_review_people = models.ForeignKey(User, null=True, related_name="reviewer")
    vul_time = models.DateTimeField(auto_now_add=True)
    vul_image = models.ImageField(upload_to='vul/%Y/%m', verbose_name="复现图", null=True, blank=True)
    vul_fix = models.TextField(null=True)
    vul_frist = models.BooleanField(default=False)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.vul_url + "：" + self.get_vul_type_display()
