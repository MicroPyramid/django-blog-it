from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^blog/category/(?P<category_slug>[-\w]+)/$', selected_category,
        name='selected_category'),
    url(r'^blog/tags/(?P<tag_slug>[-\w]+)/$',
        selected_tag, name='selected_tag'),
    url(r'^blog/(?P<year>\w{0,})/(?P<month>\w{0,})/$',
        archive_posts, name='archive_posts'),
    url(r'^blog/(?P<blog_slug>[-\w]+)/$',
        blog_post_view, name='blog_post_view'),
]
