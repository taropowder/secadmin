from django.contrib import admin
from .models import Blog, CTF_learning, ON_DUTY, Book, VulRecord, WeekLearn, WeekTask

# Register your models here.
admin.site.register(Blog)
admin.site.register(CTF_learning)
admin.site.register(ON_DUTY)
admin.site.register(Book)
admin.site.register(WeekLearn)
admin.site.register(WeekTask)


@admin.register(VulRecord)
class VulRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'vul_finder', 'vul_review_people', 'vul_review')
    list_display_links = ('id', 'title')
    list_filter = ('vul_review', 'vul_type', 'vul_finder', 'vul_review_people')

    def title(self, obj):
        return obj.vul_url + "：" + obj.get_vul_type_display()
