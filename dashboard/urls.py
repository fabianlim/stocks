from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^dashboard/',
                           views.dashboard,
                           name='dashboard'),
                       url(r'^search/',
                           views.search,
                           name='search'),
                       url(r'^sidebar/',
                           views.sidebar,
                           name='sidebar'),
                       )
#                       url(r'^dashboard\?(?P<dash_params>\S+)/$',
#                           views.dashboard,
#                           name='dashboard'),
#                       url(r'^search=(?P<searchstr>\S*)\?(?P<dash_params>\S+)/$',
#                           views.search,
#                           name='search'),
