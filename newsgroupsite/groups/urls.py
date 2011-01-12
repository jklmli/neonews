from django.conf.urls.defaults import *

urlpatterns = patterns('groups.views',
    (r'^$', 'groups'),
    (r'^(?P<group_name>[\w\.]+)/$', 'threads'),
    (r'^([\w\.]+)/(?P<thread_id>\d+)/$', 'thread'),
)
