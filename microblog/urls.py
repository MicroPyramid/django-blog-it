from django.conf.urls import include, patterns, url
from .views import blog, blog_add, view_blog, delete_blog, edit_blog, categories,add_category, edit_category, delete_category

urlpatterns = patterns('',
    url(r'^$', blog, name='blog'),
    url(r'^add/$', blog_add, name='blog_add'),
    url(r'^view/(?P<blog_id>[0-9]+)/$', view_blog, name='view_blog'),
    url(r'^delete/(?P<blog_id>[0-9]+)/$', delete_blog, name='delete_blog'),
    url(r'^edit/(?P<blog_id>[0-9]+)/$', edit_blog, name='edit_blog'),
    url(r'^add_category/$', add_category, name='add_category'),
    url(r'^category/$', categories, name='categories'),
    url(r'^delete_category/(?P<category_id>[0-9]+)/$', delete_category, name='delete_category'),
    url(r'^edit_category/(?P<category_id>[0-9]+)/$', edit_category, name='edit_category'),

)