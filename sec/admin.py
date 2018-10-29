from django.contrib import admin
from .models import Blog, CTF_learning, ON_DUTY, Book, VulRecord, WeekLearn, WeekTask
from .models import BlogDirection, UserProfile
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




# Register your models here.
admin.site.register(Blog)
admin.site.register(CTF_learning)
admin.site.register(ON_DUTY)
admin.site.register(Book)
admin.site.register(WeekTask)
admin.site.register(BlogDirection)
admin.site.site_title = "711综合管理系统"
admin.site.site_header = "711综合管理系统"
admin.site.index_title = "711综合管理系统"


@admin.register(VulRecord)
class VulRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'vul_finder', 'vul_review_people', 'vul_review')
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
        # return str(obj.learn_task.get_task_direction_display())
        return str(obj.learn_task)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'phone', 'direction')
    list_display_links = ('id', 'name')
    list_filter = ('direction', 'grade')

    def name(self, obj):
        return str(obj.user) + "：" + str(obj.user.first_name)