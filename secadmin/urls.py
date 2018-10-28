"""secadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from sec import views, vul, weeklearn
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home),
    url(r'^submit_week_learn/', weeklearn.submit_week_learn),
    url(r'^changepersion/', views.change_persion),
    url(r'^week_list/', weeklearn.week_list),
    url(r'^submit/', views.submit),
    url(r'^vul_review/$', vul.vul_review),
    url(r'^vul_add/$', vul.vul_add),
    url(r'^vul_reviewed/', vul.vul_reviewed),
    url(r'^my_vul/', vul.my_vul),
    url(r'^ranking/', vul.ranking),
    url(r'^login/', views.user_login),
    url(r'^changeblog/', views.changeblog),
    url(r'^random_week/', views.random_week),
    url(r'^change/(\d+)/', views.change, name='change_id'),
    url(r'^register/', views.register),
    url(r'^blog/(\d+)/$', views.weekblog, name='week'),
    url(r'^myblog/(\d+)/$', views.myblog, name='user_id'),
    url(r'^logout/', views.user_logout),
    url(r'^search/', views.search),
    url(r'^classification/', views.classification),
    url(r'^onduty/', views.onduty),
    url(r'^ctflerning/', views.ctflerning),
    url(r'^book/', views.book),
    url(r'^lend/', views.lend),
    url(r'^back/', views.back),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
