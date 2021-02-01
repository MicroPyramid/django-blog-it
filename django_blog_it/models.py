import arrow
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

BLOG_STATUS_CHOICE = (
    ('Drafted', 'Drafted'),
    ('Published', 'Published'),
    ('Trashed', 'Trashed'),
    ('Review', 'Review')
)

ROLE_CHOICE = (
    ('Blog Admin', 'blog_admin'),
    ('Blog Publisher', 'blog_publisher'),
    ('Blog Author', 'blog_author'),
)


class BlogUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="user_roles")
    role = models.CharField(max_length=200, choices=ROLE_CHOICE,
                            default='blog_author')
    is_active = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    meta_description = models.TextField(max_length=160, null=True, blank=True)
    meta_keywords = models.TextField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def category_posts(self):
        return Article.objects.filter(category=self).count()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        tempslug = slugify(self.name)
        if self.id:
            tag = Tag.objects.get(pk=self.id)
            if tag.name != self.name:
                self.slug = create_tag_slug(tempslug)
        else:
            self.slug = create_tag_slug(tempslug)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def create_tag_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Tag.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='related_posts')
    status = models.CharField(
        max_length=10, choices=BLOG_STATUS_CHOICE, default='Drafted')
    publish_on = models.DateField()
    meta_description = models.TextField(max_length=160, null=True, blank=True)
    meta_keywords = models.TextField(max_length=255, null=True, blank=True)
    meta_author = models.TextField(max_length=255, null=True, blank=True)
    is_page = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def create_activity(self, user, content):
        return History.objects.create(
            user=user, post=self, content=content
        )

    def create_activity_instance(self, user, content):
        return History(
            user=user, post=self, content=content
        )

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def published_on_arrow(self):
        return arrow.get(self.publish_on).humanize()


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Article.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(
        Article, related_name='history', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_page = models.BooleanField(default=False)

    def __str__(self):
        return '{username} {content} {blog_title}'.format(
            username=str(self.user.get_username()),
            content=str(self.content),
            blog_title=str(self.post.title)
        )
