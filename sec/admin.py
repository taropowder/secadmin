from django.contrib import admin
from .models import Blog, CTF_learning, ON_DUTY, Book, VulRecord, WeekLearn, WeekTask
from .models import BlogDirection, UserProfile
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
    list_display = ('id', 'learner', 'learn_time', 'learn_week')
    list_display_links = ('id', 'learner')
    list_filter = ('learner', 'learn_week')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'phone', 'direction')
    list_display_links = ('id', 'name')
    list_filter = ('direction', 'grade')

    def name(self, obj):
        return str(obj.user) + "：" + str(obj.user.first_name)