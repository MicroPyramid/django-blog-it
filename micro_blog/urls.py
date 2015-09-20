"""micro_blog URL Configuration

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
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from .settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r"^blog/", include('microblog.urls', namespace='blog')),
              ] + static(MEDIA_URL, document_root=MEDIA_ROOT)

import os

urlpatterns += patterns('',
                        (r'^media/(.*)$', 'django.views.static.serve',
                         {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
                        )
