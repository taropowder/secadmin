# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#
class BlogDirection(models.Model):
    DIRECTION_CHOICES = (
        ('sec', '网络安全'),
        ('dat', '大数据'),
    )
    name = models.CharField("名称", max_length=10)
    direction = models.CharField("方向", max_length=10, choices=DIRECTION_CHOICES)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name

    class Meta:
        verbose_name_plural = '博客方向'


class Blog(models.Model):
    blog_user = models.ForeignKey(User)
    content = models.TextField("博客标题", null=False)
    direction = models.CharField("方向（已弃用，移植到新的博客方向）", max_length=30, null=True)
    new_direction = models.ForeignKey(BlogDirection, null=True)
    url = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField("周数")

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.content

    class Meta:
        verbose_name_plural = '博客'
        ordering = ["-time"]


class CTF_learning(models.Model):
    title = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    type = models.CharField(max_length=20)

    class Meta:
        # 末尾不加s
        verbose_name_plural = 'CTF资料库'

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.title


class ON_DUTY(models.Model):
    time = models.CharField(max_length=30)
    name = models.CharField(max_length=100)

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.time

    class Meta:
        verbose_name_plural = '值班表'


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

    class Meta:
        verbose_name_plural = '图书管理'


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

    class Meta:
        verbose_name_plural = '漏洞记录管理'


class WeekTask(models.Model):
    DIRECTION_CHOICES = (
        ('sec', '网络安全'),
        ('dat', '大数据'),
    )
    task_content = models.TextField()
    task_week = models.IntegerField()
    task_direction = models.CharField("方向", max_length=10, choices=DIRECTION_CHOICES, default='sec')

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.task_week)

    class Meta:
        verbose_name_plural = '每周任务'


class WeekLearn(models.Model):
    learner = models.ForeignKey(User)
    learn_image = models.ImageField(upload_to='learn/%Y/%m', verbose_name="复现图", null=True, blank=True)
    learn_time = models.DateTimeField(auto_now_add=True)
    learn_task = models.ForeignKey(WeekTask, null=True)

    class Meta:
        verbose_name_plural = '每周基础学习管理'


class UserProfile(models.Model):
    DIRECTION_CHOICES = (
        ('sec', '网络安全'),
        ('dat', '大数据'),
    )
    user = models.OneToOneField(User)  # 关联自带的User结构
    student_id = models.CharField("学号", max_length=10)
    direction = models.CharField("方向", max_length=10, choices=DIRECTION_CHOICES, default='sec')
    qq = models.CharField("QQ", max_length=14, null=True)
    phone = models.CharField("联系电话", max_length=12, null=True)
    grade = models.IntegerField("入学年份")

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.user)

    class Meta:
        verbose_name_plural = '个人信息'


class DoorCard(models.Model):
    STATUS_CHOICES = (
        ('in', '正在实验室并且已开门'),
        ('out', '离开实验室并已关门'),
        ('unknow', '离开实验室走时未关门')
    )

    owner = models.OneToOneField(User)
    number = models.CharField('编号', max_length=10)
    get_time =models.DateTimeField(auto_now=True)
    status = models.CharField("门卡状态", max_length=10, choices=STATUS_CHOICES, default='unknow')

    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return str(self.number)

    class Meta:
        verbose_name_plural = '门卡管理'