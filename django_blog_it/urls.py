from django.urls import path, re_path
from django.conf.urls.static import static
from .django_blog_it.views import *
from .posts.views import *
from .settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('blog/contact/', contact_us, name='contact_us'),
    path('blog/category/<slug:category_slug>/', SelectedCategoryView.as_view(), name='selected_category'),
    path('blog/tags/<slug:tag_slug>/', SelectedTagView.as_view(), name='selected_tag'),
    re_path(r'^blog/(?P<year>\w{0,})/(?P<month>\w{0,})/$', ArchiveView.as_view(), name='archive_posts'),
    path('blog/<slug:blog_slug>/', BlogPostView.as_view(), name='blog_post_view'),

    path('dashboard/', AdminLoginView.as_view(), name='admin_login'),
    path('dashboard/gplus/', google_login, name='google_login'),
    path('fb/', facebook_login, name='facebook_login'),
    path('dashboard/logout/',
         admin_logout,
         name='admin_logout'),
    path('dashboard/blog/',
         PostList.as_view(),
         name='blog'),
    path('dashboard/add/',
         PostCreateView.as_view(),
         name='blog_add'),
    path('dashboard/view/<slug:blog_slug>/',
         PostDetailView.as_view(),
         name='view_blog'),
    path('dashboard/delete/<slug:blog_slug>/',
         PostDeleteView.as_view(),
         name='delete_blog'),
    path('dashboard/edit/<slug:blog_slug>/',
         PostEditView.as_view(),
         name='edit_blog'),
    path('dashboard/bulk_actions_blog/',
         BlogPostBulkActionsView.as_view(),
         name='bulk_actions_blog'),

    path('dashboard/category/', CategoryList.as_view(), name='categories'),
    path('dashboard/category/add/', CategoryCreateView.as_view(), name='add_category'),
    path('dashboard/category/edit/<slug:category_slug>/', CategoryUpdateView.as_view(), name='edit_category'),
    path('dashboard/category/delete/<slug:category_slug>/', CategoryDeleteView.as_view(), name='delete_category'),
    path('dashboard/category/status/<slug:category_slug>/',
         CategoryStatusUpdateView.as_view(), name='category_status_update'),
    # pages
    path('dashboard/bulk_actions_category/',
         CategoryBulkActionsView.as_view(), name='bulk_actions_category'),

    path('dashboard/upload_photos/', upload_photos, name='upload_photos'),
    path('dashboard/recent_photos/', recent_photos, name='recent_photos'),
    path('dashboard/users/', UserListView.as_view(), name='users'),
    path('dashboard/users/add/', UserCreateView.as_view(), name='add_user'),
    path('dashboard/user/edit/<slug:pk>/', UserUpdateView.as_view(), name='edit_user'),
    path('dashboard/user/update/<slug:pk>/', user_status_update, name='user_status_update'),
    path('dashboard/user/edit/<slug:pk>/user_role/',
         edit_user_role, name='edit_user_role'),
    path('dashboard/user/delete/<slug:pk>/',
         UserDeleteView.as_view(), name='delete_user'),
    path('dashboard/bulk_actions_users/',
         UserBulkActionsView.as_view(), name='bulk_actions_users'),

    # themes management
    path('dashboard/themes/', ThemesList.as_view(), name='themes'),
    # path('dashboard/themes/add/', add_theme, name='add_theme'),
    path('dashboard/themes/add/',
         ThemeCreateView.as_view(),
         name='add_theme'),
    path('dashboard/themes/<slug:theme_slug>/',
         ThemeDetailView.as_view(),
         name='view_theme'),
    path('dashboard/themes/edit/<int:pk>/',
         ThemeUpdateView.as_view(),
         name='edit_theme'),
    # path('dashboard/themes/edit/<slug:theme_slug>/',
    #     edit_theme, name='edit_theme'),
    path('dashboard/themes/delete/<slug:pk>/',
         DeleteThemeView.as_view(),
         name='delete_theme'),
    # path('dashboard/themes/delete/<slug:theme_slug>/',
    #     delete_theme, name='delete_theme'),
    path('dashboard/bulk_actions_themes/',
         ThemesBulkActionsView.as_view(), name='bulk_actions_themes'),

    path('dashboard/themes/update/<slug:theme_slug>/',
         theme_status_update,
         name='theme_status_update'),

    path('dashboard/contactUs/',
         configure_contact_us, name='configure_contact_us'),
    path('dashboard/change-password/', ChangePasswordView.as_view(), name='change_password'),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
