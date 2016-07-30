from django.test import TestCase
from django.test import Client
from django_blog_it.django_blog_it.models import Category, Post, Tags, PostHistory, UserRole, Page
from django.contrib.auth.models import User
from django_blog_it.django_blog_it.forms import BlogCategoryForm, BlogPostForm, AdminLoginForm
from django.core.urlresolvers import reverse
from django_blog_it.django_blog_it.models import Menu, Theme
from .forms import UserForm


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
class pages_models_test(TestCase):

    def create_pages(self, title="simple page", content="simple content", meta_description="meta description", meta_title="meta title"):
        return Page.objects.create(title=title, content=content, meta_description=meta_description, meta_title=meta_title)

    def test_page_creation(self):
        w = self.create_pages()
        self.assertTrue(isinstance(w, Page))
        self.assertEqual(w.__str__(), w.title)


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

    def get_category(self):
        self.category2 = Category.objects.create(name='generators',
                                                 description='generators',
                                                 user=self.user)
        return self.category2

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'mp', 'mp')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'mp', 'mp')
        self.category = Category.objects.create(
            name='salesforce', description='salesforce desc', user=self.user, is_active=True)
        self.blogppost = Post.objects.create(
            title='python introduction',
            user=self.user,
            content='This is content',
            category=self.category,
            status='Published')

    def test_blogpostform(self):
        data = {'title': 'jquery introduction',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'is_superuser': 'True',
                'slug': 'jquery-introduction'}
        form = BlogPostForm(data=data)
        self.assertTrue(form.is_valid())
        form = BlogPostForm(data=data, user_role='Author')
        self.assertTrue(form.is_valid())

    def test_BlogCategoryForm(self):
        data = {'name': 'django form',
                'description': 'django',
                'user': self.category.id}
        form = BlogCategoryForm(data=data)
        self.assertTrue(form.is_valid())
        form = BlogCategoryForm(data=data)
        self.assertTrue(form.is_valid())
        data['name'] = 'salesforce'
        form = BlogCategoryForm(data=data)
        self.assertFalse(form.is_valid())
        data['name'] = self.category.name
        form = BlogCategoryForm(data=data, instance=self.get_category())
        self.assertFalse(form.is_valid())

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

    def tearDown(self):
        super(django_blog_it_forms_test, self).tearDown()
        if hasattr(self, 'category2'):
            self.category2.delete()


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
        self.assertTemplateUsed(response, 'dashboard/new_admin-login.html')

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
        self.assertTemplateUsed(response, 'dashboard/new_admin-login.html')

        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/view/' + str(self.blogppost.slug) + '/')
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'dashboard/blog/blog_view.html')

        response = self.client.get('/dashboard/logout/')
        self.assertEqual(response.status_code, 302)

    def test_blog_post(self):

        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/dashboard/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_list.html')

        response = self.client.post('/dashboard/blog/', {'select_status': '', 'search_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_list.html')

        response = self.client.post('/dashboard/blog/', {'select_status': 'Published', 'search_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_list.html')

        response = self.client.post(
            '/dashboard/blog/',
            {
                'select_status': 'Published',
                'search_text': str(self.category.id)
            })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_list.html')

        response = self.client.post('/dashboard/blog/', {'select_status': '', 'search_text': str(self.category.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_list.html')

        response = self.client.get('/dashboard/category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/new_categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': '', 'category': []})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/new_categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': 'True', 'category': []})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/new_categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': 'False', 'category': []})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/new_categories_list.html')

        response = self.client.post(
            '/dashboard/category/',
            {
                'select_status': 'Published',
                'category': [str(self.category.id)]
            })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/new_categories_list.html')

        response = self.client.post('/dashboard/category/', {'select_status': '', 'category': [str(self.category.id)]})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/new_categories_list.html')

        response = self.client.get('/dashboard/category/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/category/new_category_add.html')

        response = self.client.post(
            '/dashboard/category/add/',
            {
                'name': 'python',
                'description': 'Python description',
                'user': str(self.user.id)
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully added your category' in str(response.content))

        response = self.client.post(
            '/dashboard/category/add/', {'description': 'python'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully added your category' in str(response.content))

        response = self.client.get('/dashboard/category/edit/django/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/dashboard/category/edit/django/', {'name': 'django', 'description': 'django', 'user': str(self.user.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully updated your category' in str(response.content))

        response = self.client.post(
            '/dashboard/category/edit/django/', {'name': 'jquery', 'description': 'django', 'user': str(self.user.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully updated your category' in str(response.content))

        response = self.client.post(
            '/dashboard/category/edit/python/', {'description': 'python'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully updated your category' in str(response.content))

    def test_blog_with_super_admin(self):

        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/view/' + str(self.blogppost.slug) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_view.html')

        response = self.client.get('/dashboard/upload_photos/', {'CKEditorFuncNum': '/dashboard/'})
        self.assertEqual(response.status_code, 200)
        context = {'CKEditorFuncNum': '/dashboard/'}
        response = self.client.get('/dashboard/upload_photos/', context)
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
            '/dashboard/category/add/',
            {
                'name': 'python',
                'description': 'Python description',
                'user': str(self.user.id)
            })
        response = self.client.get('/dashboard/category/delete/python/')
        self.assertEqual(response.status_code, 302)


class blog_post_creation(TestCase):

    def get_author_role(self):
        self.author_role = UserRole.objects.create(user=self.user, role='Author')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'mp', 'mp')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'mp', 'mp')
        self.category = Category.objects.create(
            name='salesforce', description='salesforce desc', user=self.user, is_active=True)
        self.post = Post.objects.create(title="apache", slug="apache", category=self.category, user=self.user)

    def test_blog_post_add(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_add.html')

        response = self.client.post(
            reverse("blog_add"),
            {
                'title': 'python introduction',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'python-introduction-1',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'], 'slugs-1-slug': [''],
                'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            })
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully posted your blog' in str(response.content))

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
                'slug': 'testing',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['testing-11223'], 'slugs-1-slug': [''],
                'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            })
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully posted your blog' in str(response.content))

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
                'slug': 'nginx-post',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['testing-11223'], 'slugs-1-slug': [''],
                'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            })
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully posted your blog' in str(response.content))
        response = self.client.get(reverse("edit_blog", kwargs={"blog_slug": self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/blog/new_blog_add.html')

        response = self.client.post(
            reverse('edit_category', kwargs={"category_slug": self.category.slug}),
            {
                'title': 'nginx-post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'nginx-post',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['nginx-post-1'], 'slugs-1-slug': [''],
                'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            })
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully updated your blog post' in str(response.content))

        response = self.client.post(
            reverse("edit_blog", kwargs={"blog_slug": self.post.slug}),
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

        response = self.client.post(reverse("edit_blog", kwargs={"blog_slug": self.post.slug}), {'content': '', 'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully updated your blog post' in str(response.content))

        response = self.client.post(
            reverse("edit_blog", kwargs={"blog_slug": self.post.slug}),
            {
                'title': 'nginx-post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'django',
                'is_superuser': 'True',
                'slug': 'nginx-post-1',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on'],
                'slugs-1-id': [''], 'slugs-2-id': [''], 'slugs-3-id': [''],
            })
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully updated your blog post' in str(response.content))
        self.post = Post.objects.first()
        response = self.client.post(
            reverse("edit_blog", kwargs={"blog_slug": self.post.slug}),
            {
                'title': 'nginx-post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'nginx',
                'is_superuser': 'True',
                'slug': 'nginx-post-1',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on'],
                'slugs-1-id': [''], 'slugs-2-id': [''], 'slugs-3-id': [''],
            })
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully updated your blog post' in str(response.content))

        self.user.is_superuser = False
        self.user.save()
        self.get_author_role()
        response = self.client.post(
            reverse("edit_blog", kwargs={"blog_slug": self.post.slug}),
            {
                'title': 'nginx-post',
                'content': 'This is content',
                'category': self.category.id,
                'status': 'Published',
                'tags': 'nginx',
                'is_superuser': 'True',
                'slug': 'nginx-post-1',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on'],
                'slugs-1-id': [''], 'slugs-2-id': [''], 'slugs-3-id': [''],
            })
        self.assertEqual(response.status_code, 200)

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
                'slug': 'haystack-post',
                'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['haystack-post-1'], 'slugs-1-slug': [''],
                'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            })
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully posted your blog' in str(response.content))

        response = self.client.get(reverse("delete_category", kwargs={"category_slug": self.category.slug}))
        self.assertEqual(response.status_code, 302)
        self.post = Post.objects.create(title="apache2", slug="apache2", category=self.category, user=self.user)
        response = self.client.post(reverse("delete_blog", kwargs={"blog_slug": self.post.slug}), {'action': 'trash'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse("delete_blog", kwargs={"blog_slug": self.post.slug}), {'action': 'restore'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse("delete_blog", kwargs={"blog_slug": self.post.slug}), {'action': 'save'})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse("delete_blog", kwargs={"blog_slug": self.post.slug}), {'action': 'delete'})
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        super(blog_post_creation, self).tearDown()
        if hasattr(self, 'author_role'):
            self.author_role.delete()


class users_roles(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'mp', 'mp')
        self.user_role = UserRole.objects.create(user=self.user, role='Admin')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'mp', 'mp')
        UserRole.objects.create(user=self.employee, role='Admin')
        # self.employee_role = UserRole.objects.create(user=self.employee, role='Author')

    def test_users_list(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/user/new_list.html')

        response = self.client.get('/dashboard/users/', {'select_role': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/dashboard/users/', {'select_role': 'Admin'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/dashboard/users/', {'select_role': 'Author'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/dashboard/users/', {'select_role': 'Admin'})
        self.assertEqual(response.status_code, 200)

    def test_users_edit_delete(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/dashboard/user/edit/' + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'dashboard/user/new_user_role.html')

        response = self.client.post('/dashboard/user/edit/' + str(self.user.id) + '/', {'role': 'Publisher'})
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully Updated User Role' in str(response.content))

        response = self.client.post('/dashboard/user/edit/' + str(self.employee.id) + '/', {'role': 'Author'})
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Successfully Updated User Role' in str(response.content))

        response = self.client.post('/dashboard/user/edit/' + str(self.employee.id) + '/', {'role': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully Updated User Role' in str(response.content))

        response = self.client.get('/dashboard/user/delete/' + str(self.employee.id) + '/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/dashboard/user/delete/' + str(self.employee.id+1) + '/')
        self.assertEqual(response.status_code, 404)


class Pages(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'mp', 'mp')
        self.user_role = UserRole.objects.create(user=self.user, role='Admin')
        self.employee = User.objects.create_user(
            'mp@micropyramid.com', 'mp', 'mp')
        self.page = Page.objects.create(
            title="test", content="test content", meta_description='page desc', keywords='keywords', meta_title="meta title")

    def test_pages_list(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get(reverse('pages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/pages/new_list.html')

        response = self.client.get(reverse('pages'), {'select_status': 'True'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('pages'), {'select_status': 'False'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('bulk_actions_pages'), {'page_ids[]': [str(self.page.id)]})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('bulk_actions_pages'), {'page_ids[]': [str(self.page.id)], 'action': 'True'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('bulk_actions_pages'), {'page_ids[]': [str(self.page.id)], 'action': 'False'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('bulk_actions_pages'), {'page_ids[]': [str(self.page.id)], 'action': 'Delete'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('bulk_actions_pages'), {'action': 'Delete'})
        self.assertEqual(response.status_code, 200)

    def test_pages_add(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.post(
            reverse('add_page'),
            {
                'title': 'nginx post',
                'content': 'This is content',
                'meta_description': 'page meta data',
                'meta_title': 'meta title',
                'keywords': 'django',
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Successfully added your page' in str(response.content))

        response = self.client.post(
            reverse('add_page'),
            {
                'title': '',
                'content': 'This is content',
                'meta_description': 'page meta data',
                'meta_title': 'meta title',
                'keywords': 'django',
            })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully added your page' in str(response.content))

        response = self.client.get(reverse('add_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/pages/new_add_page.html')

        response = self.client.get(reverse('edit_page', kwargs={'page_slug': self.page.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/pages/new_add_page.html')

        response = self.client.post(
            reverse('edit_page', kwargs={'page_slug': self.page.slug}),
            {
                'title': '',
                'content': 'This is content',
                'meta_description': 'page meta data',
                'meta_title': 'meta title',
                'keywords': 'django',
            })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Successfully added your page' in str(response.content))
        response = self.client.post(
            reverse('edit_page', kwargs={'page_slug': self.page.slug}),
            {
                'title': 'Hello world',
                'content': 'This is content',
                'meta_description': 'page meta data',
                'meta_title': 'meta title',
                'keywords': 'django',
            })
        self.assertEqual(response.status_code, 200)

    def test_delete_page(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)
        response = self.client.get(reverse('delete_page', kwargs={'page_slug': self.page.slug}))
        self.assertEqual(response.status_code, 302)

    def test_delete_page_404(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)
        self.user.is_superuser = False
        self.user.save()
        response = self.client.get(reverse('delete_page', kwargs={'page_slug': self.page.slug}))
        self.assertEqual(response.status_code, 302)


class AdminLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro-test', 'mp')

    def test_admin_login(self):
        url = reverse('admin_login')
        self.client.login(username=self.user.email, password='mp')
        data = {'username': 'mp@mp.com', 'password': 'mp'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.user.is_active = False
        self.user.save()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        data['email'] = 'not@used.com'
        response = response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class TestMenu(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com',
                                                  'mp',
                                                  'mp')

    def get_menu_and_parent(self):
        menu = Menu.objects.create(title='django',
                                   url="http://www.django.com",
                                   lvl=1)
        parent = Menu.objects.create(title='jquery',
                                     url="http://www.django.com",
                                     lvl=2)
        return menu, parent

    def test_add_menu(self):
        url = reverse('add_menu')
        is_logged_in = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(is_logged_in)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = {'title': 'django', 'url': 'http://django.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_edit_menu(self):
        menu, parent = self.get_menu_and_parent()
        url = reverse('edit_menu', kwargs={'pk': menu.pk})
        is_logged_in = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(is_logged_in)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        context = {'title': 'django',
                   'url': 'http://django.com'}
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)
        context['parent'] = parent.pk
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)
        context['parent'] = menu.pk
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)
        menu.delete()
        parent.delete()


class Menus(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com',
                                                  'mp',
                                                  'mp')

    def test_menus(self):
        url = reverse('menus')
        is_logged_in = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(is_logged_in)
        context = {'select_status': 'True'}
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)
        context['select_status'] = 'False'
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)


class TestThemeCreateView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'mp', 'mp')

    def test_theme_create_view(self):
        is_logged_in = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(is_logged_in)
        url = reverse("add_theme")
        context = {
            "name": "theme-1",
            "enabled": "True",
            "description": "theme-1 description",
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)


class TestThemesList(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'mp', 'mp')

    def test_themes_list(self):
        is_logged_in = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(is_logged_in)
        url = reverse("blog")
        context = {'select_status': 'Published', "search_text": "hi"}
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)


class TestMenuStatusUpdate(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'mp', 'mp')
        self.menu = Menu.objects.create(title="menu-1", lvl=1)

    def test_menu_status_update(self):
        login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(login)
        url = reverse("menu_status_update", kwargs={"pk": self.menu.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class TestThemesBulkActionsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'mp', 'mp')
        Theme.objects.bulk_create([
            Theme(name="theme-1", slug="theme-1", description="desc", enabled=True),
            Theme(name="theme-2", slug="theme-2", description="desc", enabled=False),
            Theme(name="theme-3", slug="theme-3", description="desc", enabled=True),
            Theme(name="theme-4", slug="theme-4", description="desc", enabled=False),
        ])

    def test_bulk_actions_themes(self):
        login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(login)
        url = reverse("bulk_actions_themes")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = {"theme_ids[]": list(Theme.objects.values_list("id", flat=True)), "action": "False"}
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)
        context = {"theme_ids[]": list(Theme.objects.values_list("id", flat=True)), "action": "Delete"}
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)


class TestThemeStatusUpdate(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'mp', 'mp')
        self.theme = Theme.objects.create(name="theme-1", slug="theme-1", description="desc", enabled=True)

    def test_theme_status_change(self):
        login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(login)
        url = reverse("theme_status_update", kwargs={"theme_slug": self.theme.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        url = reverse("theme_status_update", kwargs={"theme_slug": self.theme.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_theme(self):
        login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(login)
        url = reverse("delete_theme", kwargs={"pk": self.theme.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class TestThemeUpdateView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'mp', 'mp')
        self.theme = Theme.objects.create(name="theme-1", slug="theme-1", description="desc", enabled=True)

    def test_edit_theme(self):
        login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(login)
        url = reverse("edit_theme", kwargs={"pk": self.theme.pk})
        context = {
            "name": "theme-1",
            "description": "theme-1 descripiton",
            "enabled": True
        }
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)


class TestConfigureContactUs(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'mp', 'mp')

    def test_configure_contact_us_get(self):
        login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(login)
        url = reverse("configure_contact_us")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = {
            "from_email": "admin@mp.com",
            "reply_to_email": "admin1@mp.com",
            "email_admin": "admin2@mp.com",
            "subject": "Thank you for contacting us",
            "body_user": "Thanks! We will contact you soon",
            "body_admin": "Thanks"
        }
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 200)


# test forms
class TestUserForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('mp@mp.com', 'mp@mp.com', 'mp')

    def test_user_email(self):
        form = UserForm(data={"username": "mp@mp.com", "email": "mp@mp.com"})
        self.assertFalse(form.is_valid())

    def test_user_email_instance(self):
        form = UserForm(data={"username": "mp@mp.com", "email": "mp@mp.com"}, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_user_save(self):
        form = UserForm(data={"username": "mp@mp.com", "email": "mp@mp.com", "password": "password", "role": "Admin", "code": "Admin"}, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
