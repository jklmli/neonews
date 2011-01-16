from django.conf.urls.defaults import *

urlpatterns = patterns('groups.views',
    (r'^$', 'groups'),
    (r'^(?P<group_id>\d+)/$', 'postListing'),
    (r'^(\d+)/(?P<post_id>\d+)/$', 'singlePost'),
)
