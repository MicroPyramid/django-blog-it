from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^blog/category/(?P<category_slug>[-\w]+)/$', selected_category,
                           name='selected_category'),
                       url(r'^blog/tags/(?P<tag_slug>[-\w]+)/$', selected_tag, name='selected_tag'),
                       url(r'^blog/(?P<year>\w{0,})/(?P<month>\w{0,})/$', archive_posts, name='archive_posts'),
                       )
