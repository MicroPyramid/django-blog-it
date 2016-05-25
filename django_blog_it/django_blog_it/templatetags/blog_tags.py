import datetime
from django import template
from django_blog_it.django_blog_it.models import Post, Tags, UserRole
from django_blog_it.django_blog_it.views import get_user_role

register = template.Library()


@register.assignment_tag(takes_context=True)
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
