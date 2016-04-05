from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', admin_login, name='admin_login'),
    url(r'^logout/$', admin_logout, name='admin_logout'),
    url(r'^blog/$', blog, name='blog'),
    url(r'^add/$', blog_add, name='blog_add'),
    url(r'^view/(?P<blog_slug>[-\w]+)/$', view_blog, name='view_blog'),
    url(r'^delete/(?P<blog_slug>[-\w]+)/$', delete_blog, name='delete_blog'),
    url(r'^edit/(?P<blog_slug>[-\w]+)/$', edit_blog, name='edit_blog'),
    url(r'^add_category/$', add_category, name='add_category'),
    url(r'^category/$', categories, name='categories'),
    url(r'^delete_category/(?P<category_slug>[-\w]+)/$', delete_category, name='delete_category'),
    url(r'^edit_category/(?P<category_slug>[-\w]+)/$', edit_category, name='edit_category'),

    url(r'^bulk_actions_blog/$', bulk_actions_blog, name='bulk_actions_blog'),
    url(r'^bulk_actions_category/$', bulk_actions_category, name='bulk_actions_category'),
    url(r'upload_photos/$', upload_photos, name='upload_photos'),
    url(r'recent_photos/$', recent_photos, name='recent_photos'),
]
