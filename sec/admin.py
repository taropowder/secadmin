from django.contrib import admin
from .models import Blog, CTF_learning, ON_DUTY, Book, VulRecord, WeekLearn, WeekTask
from .models import BlogDirection, UserProfile, DoorCard
from django.utils.translation import ugettext_lazy as _


class TaskListFilter(admin.SimpleListFilter):
    title = _(u'提交方向')
    parameter_name = 'direction'

    def lookups(self, request, model_admin):
        return (
            ('dat', _(u'大数据')),
            ('sec', _(u'网络安全')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sec':
            return queryset.filter(learn_task__task_direction='sec')
        if self.value() == 'dat':
            return queryset.filter(learn_task__task_direction='dat')


class BlogListFilter(admin.SimpleListFilter):
    title = _(u'提交方向')
    parameter_name = 'blog_direction'

    def lookups(self, request, model_admin):
        return (
            ('dat', _(u'大数据')),
            ('sec', _(u'网络安全')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sec':
            return queryset.filter(new_direction__direction='sec')
        if self.value() == 'dat':
            return queryset.filter(new_direction__direction='dat')


# Register your models here.

admin.site.register(CTF_learning)
admin.site.register(ON_DUTY)
admin.site.register(Book)
admin.site.register(BlogDirection)
admin.site.site_title = "711综合管理系统"
admin.site.site_header = "711综合管理系统"
admin.site.index_title = "711综合管理系统"


@admin.register(DoorCard)
class DoorCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'get_time', 'status')
    list_display_links = ('number',)

    def name(self, obj):
        return str(obj.owner) + "：" + str(obj.owner.first_name)


@admin.register(VulRecord)
class VulRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'vul_finder', 'vul_ac', 'vul_au', 'vul_review_people', 'vul_review')
    list_display_links = ('id', 'title')
    list_filter = ('vul_review', 'vul_type', 'vul_finder', 'vul_review_people')

    def title(self, obj):
        return obj.vul_url + "：" + obj.get_vul_type_display()
    

@admin.register(WeekLearn)
class WeekLearnAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'learn_time', 'learn_task', 'direction_task')
    list_display_links = ('id', 'name')
    list_filter = (TaskListFilter, 'learn_task')

    def name(self, obj):
        return str(obj.learner) + "：" + str(obj.learner.first_name)

    def direction_task(self, obj):
        if obj.learn_task:
            return str(obj.learn_task.get_task_direction_display())
        else:
            return "unkonw"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'grade', 'phone', 'direction')
    list_display_links = ('student_id', 'name')
    list_filter = ('direction', 'grade')

    def name(self, obj):
        return str(obj.user) + "：" + str(obj.user.first_name)


@admin.register(WeekTask)
class WeekTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_week', 'task_direction')
    list_display_links = ('id', 'task_week')
    list_filter = ('task_direction',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('content', 'name', 'week', 'time', 'new_direction', 'direction_task')
    list_display_links = ('content',)
    list_filter = ('new_direction', BlogListFilter, 'week')

    def name(self, obj):
        return str(obj.blog_user) + "：" + str(obj.blog_user.first_name)

    def direction_task(self, obj):
        if obj.new_direction:
            return str(obj.new_direction.get_direction_display())
        else:
            return "网络安全"
