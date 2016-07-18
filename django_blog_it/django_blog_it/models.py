import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    meta_description = models.TextField(max_length=160, null=True, blank=True)
    meta_keywords = models.TextField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def category_posts(self):
        return Post.objects.filter(category=self).count()


class Tags(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        tempslug = slugify(self.name)
        if self.id:
            tag = Tags.objects.get(pk=self.id)
            if tag.name != self.name:
                self.slug = create_tag_slug(tempslug)
        else:
            self.slug = create_tag_slug(tempslug)
        super(Tags, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def create_tag_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Tags.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


STATUS_CHOICE = (
    ('Drafted', 'Drafted'),
    ('Published', 'Published'),
    ('Rejected', 'Rejected'),
    ('Trashed', 'Trashed'),
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    meta_description = models.TextField(max_length=160, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tags, related_name='rel_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='Drafted')
    keywords = models.TextField(max_length=500, blank=True)
    featured_image = models.ImageField(upload_to='static/blog/uploads/%Y/%m/%d/', blank=True, null=True)

    def save(self, *args, **kwargs):
        tempslug = slugify(self.title)
        if self.id:
            blogpost = Post.objects.get(pk=self.id)
            if blogpost.title != self.title:
                self.slug = create_slug(tempslug)
        else:
            self.slug = create_slug(tempslug)

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def is_deletable_by(self, user):
        if self.user == user or user.is_superuser:
            return True
        return False

    def create_activity(self, user, content):
        return PostHistory.objects.create(
            user=user, post=self, content=content
        )

    def create_activity_instance(self, user, content):
        return PostHistory(
            user=user, post=self, content=content
        )

    def remove_activity(self):
        self.history.all().delete()


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Post.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


class PostHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='history')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{username} {content} {blog_title}'.format(
            username=str(self.user.get_username()),
            content=str(self.content),
            blog_title=str(self.post.title)
        )


class Image_File(models.Model):
    upload = models.FileField(upload_to="static/uploads/%Y/%m/%d/")
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_image = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to="static/uploads/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return self.date_created

ROLE_CHOICE = (
    ('Admin', 'Admin'),
    ('Publisher', 'Publisher'),
    ('Author', 'Author'),
)


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.CharField(max_length=10, choices=STATUS_CHOICE)


class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    slug = models.SlugField()
    is_active = models.BooleanField(default=True)
    meta_description = models.TextField()
    keywords = models.TextField()
    meta_title = models.TextField()

    def save(self, *args, **kwargs):
        tempslug = slugify(self.title)
        if self.id:
            existed_page = Page.objects.get(pk=self.id)
            if existed_page.title != self.title:
                self.slug = create_slug(tempslug)
        else:
            self.slug = create_slug(tempslug)

        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Menu(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255, blank=True)
    status = models.BooleanField(default=True)
    lvl = models.IntegerField(blank=True)

    def __str__(self):
        return self.title

    def get_children(self):
        return self.menu_set.all()

    def has_children(self):
        if self.get_children():
            return True
        return False


class ContactUsSettings(models.Model):
    from_email = models.EmailField()
    reply_to_email = models.EmailField(blank=True, null=True)
    email_admin = models.EmailField()
    subject = models.CharField(max_length=500)
    body_user = models.TextField()
    body_admin = models.TextField()
