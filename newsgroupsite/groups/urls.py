from django.conf.urls.defaults import *

urlpatterns = patterns('groups.views',
    (r'^$', 'index'),
    (r'^(?P<group_id>\d+)/$', 'threads'),
)
