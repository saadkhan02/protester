from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^testSuites/(?P<suite_name_slug>[\w\-]+)/$', views.testSuiteDetails,
        name='testSuiteDetails'),
    url(r'^testCases/$', views.testCases, name='testCases'),
    url(r'^testSuites/$', views.testSuites, name='testSuites'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^$', views.login, name='login'),
]
