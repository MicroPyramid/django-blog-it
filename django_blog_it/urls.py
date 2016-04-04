"""django_blog_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from .django_blog_it.views import *
from .posts.views import *
from .settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^blog/category/(?P<category_slug>[-\w]+)/$', selected_category, name='selected_category'),
    url(r'^blog/tags/(?P<tag_slug>[-\w]+)/$', selected_tag, name='selected_tag'),
    url(r'^blog/(?P<year>\w{0,})/(?P<month>\w{0,})/$', archive_posts, name='archive_posts'),
    url(r'^blog/(?P<blog_slug>[-\w]+)/$', blog_post_view, name='blog_post_view'),
    url(r'^dashboard/$', admin_login, name='admin_login'),
    url(r'^dashboard/logout/$', admin_logout, name='admin_logout'),
    url(r'^dashboard/blog/$', blog, name='blog'),
    url(r'^dashboard/add/$', blog_add, name='blog_add'),
    url(r'^dashboard/view/(?P<blog_slug>[-\w]+)/$', view_blog, name='view_blog'),
    url(r'^dashboard/delete/(?P<blog_slug>[-\w]+)/$', delete_blog, name='delete_blog'),
    url(r'^dashboard/edit/(?P<blog_slug>[-\w]+)/$', edit_blog, name='edit_blog'),
    url(r'^dashboard/add_category/$', add_category, name='add_category'),
    url(r'^dashboard/category/$', categories, name='categories'),
    url(r'^dashboard/delete_category/(?P<category_slug>[-\w]+)/$', delete_category, name='delete_category'),
    url(r'^dashboard/edit_category/(?P<category_slug>[-\w]+)/$', edit_category, name='edit_category'),

    url(r'^dashboard/bulk_actions_blog/$', bulk_actions_blog, name='bulk_actions_blog'),
    url(r'^dashboard/bulk_actions_category/$', bulk_actions_category, name='bulk_actions_category'),
    url(r'^dashboard/upload_photos/$', upload_photos, name='upload_photos'),
    url(r'^dashboard/recent_photos/$', recent_photos, name='recent_photos'),
    url(r'^dashboard/users/$', users, name='users'),
    url(r'^dashboard/user/edit/(?P<pk>[-\w]+)/$', edit_user_role, name='edit_user_role'),
    url(r'^dashboard/user/delete/(?P<pk>[-\w]+)/$', delete_user, name='delete_user'),


] + static(MEDIA_URL, document_root=MEDIA_ROOT)
