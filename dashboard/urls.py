from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'dashboard\?(?P<params>\S+)/$',
                           views.dashboard),
                       url(r'search=(?P<searchstr>\S+)\?(?P<params>\S+)/$',
                           views.search),
                       )
