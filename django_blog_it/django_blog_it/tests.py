from django.test import TestCase
from django.test import Client
from django_blog_it.django_blog_it.models import Category, Post, Tags, PostHistory, UserRole
from django.contrib.auth.models import User
from django_blog_it.django_blog_it.forms import BlogCategoryForm, BlogPostForm, AdminLoginForm


# models test
class category_models_test(TestCase):

    def create_category(self, name="simple page", description="simple page content"):
        user = User.objects.create_superuser('mp@mp.com', 'micro-test', 'mp')
        return Category.objects.create(name=name, description=description, user=user)

    def test_category_creation(self):
        w = self.create_category()
        self.assertTrue(isinstance(w, Category))
        self.assertEqual(w.__str__(), w.name)


# models test
class tags_models_test(TestCase):

    def create_tags(self, name="simple page"):
        return Tags.objects.create(name=name)

    def test_category_creation(self):
        w = self.create_tags()
        self.assertTrue(isinstance(w, Tags))
        self.assertEqual(w.__str__(), w.name)


# models test
class post_models_test(TestCase):

    def create_post(
            self,
            tag="simple page",
            category="simple page",
            description="simple page content",
            title="post",
            content="content",
            status="D"
            ):
        user = User.objects.create_superuser('mp@mp.com', 'micro-test', 'mp')
        category = Category.objects.create(name=category, description=description, user=user)
        tag = Tags.objects.create(name=tag)
        return Post.objects.create(category=category, user=user, content=content, title=title, status=status)

    def test_category_creation(self):
        w = self.create_post()
        self.assertTrue(isinstance(w, Post))
        self.assertEqual(w.__str__(), w.title)


class post_history_models_test(TestCase):

    def create_post_history(self, content="simple content"):
        user = User.objects.create_superuser('mp@mp.com', 'micro-test', 'mp')
        category = Category.objects.create(name='category', description='description', user=user)
        post = Post.objects.create(category=category, user=user, content='content', title='title', status='Published')

        return PostHistory.objects.create(content=content, post=post, user=user)

    def test_category_creation(self):
        w = self.create_post_history()
        self.assertTrue(isinstance(w, PostHistory))
        self.assertEqual(w.__str__(), str(w.user.get_username()) + ' ' + str(w.content) + ' ' + str(w.post.title))


# class image_file_models_test(TestCase):

#     def create_image_file(self, content="simple content"):
#         upload_file = open('/django_blog_it/static/favicon.png', 'rb')
#         return Image_File.objects.create(Image_File=upload_file, thumbnail=upload_file, upload=upload_file)

#     def test_category_creation(self):
#         w = self.create_image_file()
#         self.assertTrue(isinstance(w, Image_File))
#         self.assertEqual(w.__str__(), str(w.date_created()))


class django_blog_it_forms_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'mp', 'mp')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'mp', 'mp')
        self.category = Category.objects.create(
            name='salesforce', description='salesforce desc', user=self.user)
        self.blogppost = Post.objects.create(
            title='python introduction',
            user=self.user,
            content='This is content',
            category=self.category,
            status='Published')

    def test_blogpostform(self):
        form = BlogPostForm(
            data={
                'title': 'jquery introduction',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'is_superuser': 'True',
                'slug': 'jquery-introduction'
            })
        self.assertTrue(form.is_valid())

    def test_BlogCategoryForm(self):
        form = BlogCategoryForm(
            data={'name': 'django form', 'description': 'django', 'user': self.category.id})
        self.assertTrue(form.is_valid())

        form = BlogCategoryForm(
            data={'name': 'django form', 'description': 'django', 'user': self.category.id})
        self.assertTrue(form.is_valid())

    def test_AdminLoginForm(self):
        form = AdminLoginForm(
            data={'username': 'mp@mp.com', 'password': 'mp'})
        self.assertTrue(form.is_valid())

        form = AdminLoginForm(
            data={'username': 'mp@mp.com', 'password': 'mp123'})
        self.assertFalse(form.is_valid())

        form = AdminLoginForm(
            data={'username': 'mp@micropyramid.com', 'password': 'mp'})
        self.assertTrue(form.is_valid())


class django_blog_it_views_get(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'micro-test', 'mp')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'micro', 'mp')
        self.category = Category.objects.create(
            name='django', description='django desc', user=self.user, is_active=True)
        self.linuxcategory = Category.objects.create(
            name='linux', description='django desc', user=self.user, is_active=True)
        self.blogppost = Post.objects.create(
            title='other python introduction',
            user=self.user,
            content='This is content',
            category=self.category,
            status='Published',
            slug="other-python-introduction")
        self.tag = Tags.objects.create(name='testtag')
        self.blogppost.tags.add(self.tag)
        self.pythonpost = Post.objects.create(
            title='decorator',
            user=self.user,
            content='This is content',
            category=self.category,
            status='Published',
            slug="decorator")

    def test_blog_get(self):

        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/admin-login.html')

        response = self.client.post(
            '/dashboard/', {'email': 'mp@mp.com', 'password': 'micro-test'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/dashboard/', {'email': 'mp@mp.com', 'password': 'micro'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/dashboard/', {'email': 'mp@micropyramid.com', 'password': 'micro'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/dashboard/', {'email': 'mp@micropyramid.com', 'password': 'micro-test'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/admin-login.html')

        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/view/' + str(self.blogppost.slug) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_view.html')

        response = self.client.get('/dashboard/logout/')
        self.assertEqual(response.status_code, 302)

    def test_blog_post(self):

        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/dashboard/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_list.html')

        response = self.client.post('/dashboard/blog/', {'select_status': '', 'search_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_list.html')

        response = self.client.post('/dashboard/blog/', {'select_status': 'Published', 'search_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_list.html')

        response = self.client.post(
            '/dashboard/blog/',
            {
                'select_status': 'Published',
                'search_text': str(self.category.id)
            })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_list.html')

        response = self.client.post('/dashboard/blog/', {'select_status': '', 'search_text': str(self.category.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_list.html')

        response = self.client.get('/dashboard/category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': '', 'category': []})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': 'True', 'category': []})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': 'False', 'category': []})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/categories_list.html')

        response = self.client.post(
            '/dashboard/category/',
            {
                'select_status': 'Published',
                'category': [str(self.category.id)]
            })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': '', 'category': [str(self.category.id)]})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/categories_list.html')

        response = self.client.get('/dashboard/add_category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/category_add.html')

        response = self.client.post(
            '/dashboard/add_category/',
            {
                'name': 'python',
                'description': 'Python description',
                'user': str(self.user.id)
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully added your category' in str(response.content))

        response = self.client.post(
            '/dashboard/add_category/', {'description': 'python'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully added your category' in str(response.content))

        response = self.client.get('/dashboard/edit_category/django/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/dashboard/edit_category/django/', {'name': 'django', 'description': 'django', 'user': str(self.user.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully updated your category' in str(response.content))

        response = self.client.post(
            '/dashboard/edit_category/django/', {'name': 'jquery', 'description': 'django', 'user': str(self.user.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully updated your category' in str(response.content))

        response = self.client.post(
            '/dashboard/edit_category/python/', {'description': 'python'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully updated your category' in str(response.content))

    def test_blog_with_super_admin(self):

        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/view/' + str(self.blogppost.slug) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_view.html')

        response = self.client.get('/dashboard/upload_photos/', {'CKEditorFuncNum': '/dashboard/'})
        self.assertEqual(response.status_code, 200)

        # recent photos
        response = self.client.get('/dashboard/recent_photos/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/browse.html')

        response = self.client.get('/dashboard/bulk_actions_blog/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/dashboard/bulk_actions_blog/', {'blog_ids[]': [str(self.blogppost.id)]})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/dashboard/bulk_actions_blog/',
            {
                'blog_ids[]': [str(self.blogppost.id)],
                'action': 'Published'
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/dashboard/bulk_actions_blog/',
            {
                'blog_ids[]': [str(self.pythonpost.id)],
                'action': 'Delete'
            })
        self.assertEqual(response.status_code, 200)

        # bulk actions category
        response = self.client.get('/dashboard/bulk_actions_category/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/dashboard/bulk_actions_category/', {'blog_ids[]': [str(self.category.id)]})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/dashboard/bulk_actions_category/',
            {
                'blog_ids[]': [str(self.category.id)],
                'action': 'True'
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/dashboard/bulk_actions_category/',
            {
                'blog_ids[]': [str(self.linuxcategory.id)],
                'action': 'Delete'
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/dashboard/bulk_actions_category/',
            {
                'blog_ids[]': [str(self.category.id)],
                'action': 'False'
            })
        self.assertEqual(response.status_code, 200)

        # delete category
        response = self.client.post(
            '/dashboard/add_category/',
            {
                'name': 'python',
                'description': 'Python description',
                'user': str(self.user.id)
            })
        response = self.client.post('/dashboard/delete_category/python/')
        self.assertEqual(response.status_code, 302)


class blog_post_creation(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'mp', 'mp')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'mp', 'mp')
        self.category = Category.objects.create(
            name='salesforce', description='salesforce desc', user=self.user)

    def test_blog_post_add(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_add.html')

        response = self.client.post(
            '/dashboard/add/',
            {
                'title': 'python introduction',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'python-introduction-1'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully posted your blog' in str(response.content))

        response = self.client.post(
            '/dashboard/add/',
            {
                'title': 'python introduction',
                'content': '',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'python-introduction-1'
            })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully posted your blog' in str(response.content))

        response = self.client.post('/dashboard/add/', {'content': '', 'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully posted your blog' in str(response.content))

        response = self.client.post(
            '/dashboard/add/',
            {
                'title': 'testing',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'testing'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully posted your blog' in str(response.content))

    def test_blog_post_edit(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.post(
            '/dashboard/add/',
            {
                'title': 'nginx post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'nginx-post'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully posted your blog' in str(response.content))

        response = self.client.get('/dashboard/edit/nginx-post/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/blog_add.html')

        response = self.client.post(
            '/dashboard/edit/nginx-post/',
            {
                'title': 'nginx-post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'nginx-post'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully updated your blog post' in str(response.content))

        response = self.client.post(
            '/dashboard/edit/nginx-post-1/',
            {
                'title': 'nginx-post',
                'content': '',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'nginx-post-1'
            })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully updated your blog post' in str(response.content))

        response = self.client.post('/dashboard/edit/nginx-post-1/', {'content': '', 'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully updated your blog post' in str(response.content))

        response = self.client.post(
            '/dashboard/edit/nginx-post-1/',
            {
                'title': 'nginx-post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'nginx-post-1'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully updated your blog post' in str(response.content))

        response = self.client.post(
            '/dashboard/edit/nginx-post-1/',
            {
                'title': 'nginx-post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'nginx',
                'is_superuser': 'True',
                'slug': 'nginx-post-1'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully updated your blog post' in str(response.content))

    def test_blog_post_delete(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.post(
            '/dashboard/add/',
            {
                'title': 'haystack post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'haystack-post'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully posted your blog' in str(response.content))

        response = self.client.get('/dashboard/delete/haystack-post/')
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/dashboard/delete/haystack-post/', {'action': 'trash'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/dashboard/delete/haystack-post/', {'action': 'restore'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/dashboard/delete/haystack-post/', {'action': 'save'})
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/dashboard/delete/haystack-post/', {'action': 'delete'})
        self.assertEqual(response.status_code, 302)


class users_roles(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'mp', 'mp')
        self.user_role = UserRole.objects.create(user=self.user, role='Admin')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'mp', 'mp')
        # self.employee_role = UserRole.objects.create(user=self.employee, role='Author')

    def test_users_list(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/user/list.html')

        response = self.client.get('/dashboard/users/', {'select_role': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/dashboard/users/', {'select_role': 'Admin'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/dashboard/users/', {'select_role': 'Author'})
        self.assertEqual(response.status_code, 200)

    def test_users_edit_delete(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/user/edit/' + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/user/user_role.html')

        response = self.client.post('/dashboard/user/edit/' + str(self.user.id) + '/', {'role': 'Publisher'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully Updated User Role' in str(response.content))

        response = self.client.post('/dashboard/user/edit/' + str(self.employee.id) + '/', {'role': 'Author'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully Updated User Role' in str(response.content))

        response = self.client.post('/dashboard/user/edit/' + str(self.employee.id) + '/', {'role': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully Updated User Role' in str(response.content))

        response = self.client.post('/dashboard/user/delete/' + str(self.employee.id) + '/')
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/dashboard/user/delete/' + str(self.employee.id+1) + '/')
        self.assertEqual(response.status_code, 404)
