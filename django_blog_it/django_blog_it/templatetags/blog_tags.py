import datetime
import os
from django import template
from django_blog_it.django_blog_it.models import Post, Tags, Menu
from django_blog_it.django_blog_it.views import get_user_role
from django_blog_it import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_archives(context):
    archives = []
    dates = []
    for each_object in Post.objects.filter(category__is_active=True, status="Published").order_by('created_on').values('created_on'):
        for date in each_object.values():
            dates.append((date.year, date.month, 1))

    dates = list(set(dates))
    dates.sort(reverse=True)
    for each in dates:
        archives.append(datetime.datetime(each[0], each[1], each[2]))

    if len(archives) > 5:
        return archives[:5]
    return archives


@register.filter
def seperate_tags(tags):
    if tags:
        tags_list = tags.split(',')
        real_tags = []
        for tag in tags_list:
            real_tags.append(Tags.objects.get(name=tag))
        return real_tags
    return None


@register.filter
def is_deletable_by(blog_post, user):
    return blog_post.is_deletable_by(user)


@register.filter
def get_user_role_name(user):
    return get_user_role(user)


@register.filter
def get_range(value):
    return range(value)


@register.inclusion_tag('posts/new_nav_menu.html', takes_context=True)
def load_menu(context):
    context['menu'] = Menu.objects.filter(parent=None, status=True).order_by("lvl")
    return context


@register.filter
def posts_published_list(blogs_list):
    return len(blogs_list.filter(status='Published'))


@register.filter
def user_drafted_posts(user):
    return Post.objects.filter(user=user, status='Drafted').count()


@register.filter
def user_published_posts(user):
    return Post.objects.filter(user=user,
                               status='Published'
                               ).count()


@register.simple_tag
def blog_title():
    return settings.BLOG_TITLE


@register.filter
def category_posts(category):
    return Post.objects.filter(category=category).count()


@register.simple_tag
def google_analytics_id():
    return os.getenv("GOOGLE_ANALYTICS_ID")
