from django.urls import path
from .views import (dashboard, user_list, user_role,
                    blog_list, blog_new, blog_preview,
                    blog_edit, blog_delete, blog_category,
                    blog_category_list, blog_catergory_edit,
                    blog_detail, page_detail,
                    blog_category_delete, blog_content_edit_with_grapejs,
                    get_blog_content, blog_content_edit_with_ckeditor)

from django_blog_it.sitemaps import sitemap_xml
from django.conf.urls import url

app_name = "django_blog_it"

urlpatterns = [
    path('blog/admin/', dashboard, name='dashboard'),
    path('blog/admin/users/', user_list, name='user_list'),
    path('blog/admin/roles/', user_role, name='user_role'),
    path('blog/admin/articles/', blog_list, name='blog_list'),
    path('blog/admin/new-article/', blog_new, name='blog_new'),
    path('blog/admin/preview/<int:pk>/', blog_preview, name='blog_preview'),
    path('blog/admin/<int:pk>/edit/', blog_edit, name='blog_edit'),
    path('blog/admin/<int:pk>/content-edit-grapejs/', blog_content_edit_with_grapejs, name='blog_content_edit_grapejs'),
    path('blog/admin/<int:pk>/content-edit-ckeditor/', blog_content_edit_with_ckeditor, name='blog_content_edit_ckeditor'),
    path('blog/admin/<int:pk>/preview/', get_blog_content, name='get_blog_content'),
    path('blog/admin/<int:pk>/delete/', blog_delete, name='blog_delete'),
    path('blog/admin/catergory/', blog_category, name='blog_category'),
    path('blog/admin/catergory/list/',
         blog_category_list, name='blog_category_list'),
    path('blog/admin/catergory/<int:pk>/edit/',
         blog_catergory_edit, name='blog_catergory_edit'),
    path('blog/admin/catergory/<int:pk>/delete/',
         blog_category_delete, name='blog_category_delete'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('<slug:slug>/', page_detail, name='page_detail'),
    url(r'^blog/sitemap.xml$', sitemap_xml, name="sitemap_xml"),
]
