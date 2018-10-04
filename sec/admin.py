from django.contrib import admin
from .models import Blog,CTF_learning,ON_DUTY,Book,VulRecord

# Register your models here.
admin.site.register(Blog)
admin.site.register(CTF_learning)
admin.site.register(ON_DUTY)
admin.site.register(Book)
admin.site.register(VulRecord)