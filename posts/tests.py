from django.test import TestCase
from django.test import Client
from django_blog_it.django_blog_it.models import Category, Post, Tags
from django.contrib.auth.models import User


class posts_views_get(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'micro-test', 'mp')
        self.category = Category.objects.create(
            name='django', description='django desc', user=self.user, is_active=True)
        self.blogppost = Post.objects.create(
            title='other python introduction',
            user=self.user,
            content='This is content',
            category=self.category,
            status='Published',
            slug="other-python-introduction")
        self.tag = Tags.objects.create(name='testtag')
        self.blogppost.tags.add(self.tag)

    def test_blog_get(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/new_index.html')

        response = self.client.get('/blog/'+str(self.blogppost.slug)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/new_blog_view.html')

        response = self.client.get('/blog/category/'+str(self.category.slug)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/new_index.html')

        response = self.client.get('/blog/tags/'+str(self.tag.slug)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/new_index.html')

        response = self.client.get(
            '/blog/'+str(self.blogppost.updated_on.year)+'/'+str(self.blogppost.updated_on.month)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/new_index.html')
