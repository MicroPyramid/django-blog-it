from django.conf.urls import url
from django.conf.urls.static import static
from .django_blog_it.views import *
from .posts.views import *
from .settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    url(r'^$', Home.as_view(), name='index'),
    url(r'^blog/category/(?P<category_slug>[-\w]+)/$', SelectedCategoryView.as_view(), name='selected_category'),
    url(r'^blog/tags/(?P<tag_slug>[-\w]+)/$', SelectedTagView.as_view(), name='selected_tag'),
    url(r'^blog/(?P<year>\w{0,})/(?P<month>\w{0,})/$', ArchiveView.as_view(), name='archive_posts'),
    url(r'^blog/(?P<blog_slug>[-\w]+)/$', BlogPostView.as_view(), name='blog_post_view'),

    url(r'^dashboard/$', AdminLoginView.as_view(), name='admin_login'),
    url(r'^dashboard/logout/$',
        admin_logout,
        name='admin_logout'),
    url(r'^dashboard/blog/$',
        PostList.as_view(),
        name='blog'),
    url(r'^dashboard/add/$',
        PostCreateView.as_view(),
        name='blog_add'),
    url(r'^dashboard/view/(?P<blog_slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name='view_blog'),
    url(r'^dashboard/delete/(?P<blog_slug>[-\w]+)/$',
        PostDeleteView.as_view(),
        name='delete_blog'),
    url(r'^dashboard/edit/(?P<blog_slug>[-\w]+)/$',
        PostEditView.as_view(),
        name='edit_blog'),
    url(r'^dashboard/bulk_actions_blog/$',
        bulk_actions_blog,
        name='bulk_actions_blog'),

    url(r'^dashboard/category/$', CategoryList.as_view(), name='categories'),
    url(r'^dashboard/category/add/$', CategoryCreateView.as_view(), name='add_category'),
    url(r'^dashboard/category/edit/(?P<category_slug>[-\w]+)/$', CategoryUpdateView.as_view(), name='edit_category'),
    url(r'^dashboard/category/delete/(?P<category_slug>[-\w]+)/$', CategoryDeleteView.as_view(), name='delete_category'),
    # pages
    url(r'^dashboard/bulk_actions_category/$',
        bulk_actions_category, name='bulk_actions_category'),

    url(r'^dashboard/pages/$', pages, name='pages'),
    url(r'^dashboard/pages/add/$', add_page, name='add_page'),
    url(r'^dashboard/pages/edit/(?P<page_slug>[-\w]+)/$',
        edit_page, name='edit_page'),
    url(r'^dashboard/pages/delete/(?P<page_slug>[-\w]+)/$',
        delete_page, name='delete_page'),
    url(r'^dashboard/bulk_actions_pages/$',
        bulk_actions_pages, name='bulk_actions_pages'),
    url(r'^(?P<page_slug>[-\w]+)/$', PageView.as_view(), name='page_view'),

    url(r'^dashboard/upload_photos/$', upload_photos, name='upload_photos'),
    url(r'^dashboard/recent_photos/$', recent_photos, name='recent_photos'),
    url(r'^dashboard/users/$', users, name='users'),
    url(r'^dashboard/users/add/$', add_user, name='add_user'),
    url(r'^dashboard/user/edit/(?P<pk>[-\w]+)/$', edit_user, name='edit_user'),
    url(r'^dashboard/user/edit/(?P<pk>[-\w]+)/user_role/$',
        edit_user_role, name='edit_user_role'),
    url(r'^dashboard/user/delete/(?P<pk>[-\w]+)/$',
        delete_user, name='delete_user'),
    url(r'^dashboard/bulk_actions_users/$',
        bulk_actions_users, name='bulk_actions_users'),

    # menu management
    url(r'^dashboard/menu/$', menus, name='menus'),
    url(r'^dashboard/menu/add/$', add_menu, name='add_menu'),
    url(r'^dashboard/menu/edit/(?P<pk>[-\w]+)/$', edit_menu, name='edit_menu'),
    url(r'^dashboard/bulk_actions_menu/$',
        bulk_actions_menu, name='bulk_actions_menu'),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
