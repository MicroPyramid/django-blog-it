import datetime
from django import template
from microblog.models import Post, Tags

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_archives(context):
    archives = []
    dates = []
    for each_object in Post.objects.filter(status="Published").order_by('updated_on').values('updated_on'):
        for date in each_object.values():
            dates.append((date.year, date.month, 1))

    dates = list(set(dates))
    dates.sort(reverse=True)
    for each in dates:
        archives.append(datetime.datetime(each[0], each[1], each[2]))

    if len(archives) > 5:
        return archives[:5]
    return archives


@register.assignment_tag(takes_context=True)
def seperate_tags(context):
    posts_tags = Post.objects.all()
    for blog in posts_tags:
        blog_tags_new = blog.tags.split(',')
        for tag in blog_tags_new:
            real_tags = Tags.objects.get(slug=tag)
            return real_tags
